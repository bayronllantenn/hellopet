from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import SolicitudCita
from .forms import SolicitudCitaForm
from .utils import get_webpay_transaction


def index(request):
    if request.user.is_authenticated:
        try:
            perfil = request.user.perfil
            if perfil.rol == 'Recepcionista':
                return redirect('dashboard_recepcion')
            elif perfil.rol == 'Veterinario':
                return redirect('index_dr')
        except:
            pass
    return render(request, 'veterinaria/index.html')

def agendar_cita(request):
    if request.method == 'POST':
        form = SolicitudCitaForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estado = 'Pendiente'
            solicitud.estado_pago = 'Pendiente'
            solicitud.save()
            return redirect('iniciar_pago_webpay', solicitud.id)

    else:
        form = SolicitudCitaForm()
        messages.info(request, 'Complete el formulario para agendar su cita')

    return render(request, 'veterinaria/agendar/agendar_form.html', {'form': form})

# WEBPAY
def iniciar_pago_webpay(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)

    if solicitud.estado_pago == 'Pagado':
        messages.info(request, 'Esta cita ya se encuentra pagada.')
        return redirect('reserva_exitosa', solicitud.pk)

    monto = solicitud.tipo_consulta.precio_base

    buy_order = f'cita-{solicitud.pk}-{int(timezone.now().timestamp())}'
    session_id = f'sesion-{solicitud.pk}'

    return_url = request.build_absolute_uri(reverse('retorno_webpay'))

    try:
        tx = get_webpay_transaction()
        response = tx.create(buy_order=buy_order,session_id=session_id,amount=monto,return_url=return_url)
        solicitud.webpay_orden = buy_order
        solicitud.webpay_token = response['token']
        solicitud.save()

        return render(request, 'veterinaria/pago/redirigir_webpay.html', {'url': response['url'],'token': response['token']})

    except Exception as e:
        messages.error(request, f'Error al iniciar el pago: {e}')
        return redirect('reserva_fallida')


def retorno_webpay(request):
    token = request.GET.get('token_ws') or request.POST.get('token_ws')
    if not token:
        messages.error(request, 'No se recibió respuesta de Webpay.')
        return redirect('reserva_fallida')
    solicitud = SolicitudCita.objects.filter(webpay_token=token).first()
    if not solicitud:
        messages.error(request, 'No se encontró la solicitud asociada al pago.')
        return redirect('reserva_fallida')
    try:
        tx = get_webpay_transaction()
        response = tx.commit(token)
        if response.get('status') == 'AUTHORIZED':
            ya_estaba_pagado = solicitud.estado_pago == 'Pagado'
            solicitud.estado = 'Confirmada'
            solicitud.estado_pago = 'Pagado'
            solicitud.monto_pagado = solicitud.tipo_consulta.precio_base
            solicitud.fecha_pago = timezone.now()
            solicitud.save()
            if not ya_estaba_pagado and solicitud.email:
                try:
                    html_content = render_to_string('correo/cita_confirmada.html', {'solicitud': solicitud})
                    text_content = strip_tags(html_content)
                    email = EmailMultiAlternatives(subject='Cita confirmada - HelloPet', body=text_content, from_email=settings.DEFAULT_FROM_EMAIL, to=[solicitud.email])
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    messages.success(request, 'Tu cita fue reservada y pagada correctamente. Se envió un correo de confirmación.')
                except Exception as e:
                    messages.warning(request, f'Tu cita fue pagada y confirmada, pero no se pudo enviar el correo: {e}')
            else:
                messages.success(request, 'Tu cita fue reservada y pagada correctamente.')
            return redirect('reserva_exitosa', solicitud.pk)
        else:
            solicitud.estado = 'Cancelada'
            solicitud.estado_pago = 'Rechazado'
            solicitud.save()
            messages.error(request, 'El pago no fue aprobado. La cita fue cancelada.')
            return redirect('reserva_fallida_id', solicitud.pk)
    except Exception as e:
        solicitud.estado = 'Cancelada'
        solicitud.estado_pago = 'Rechazado'
        solicitud.save()
        messages.error(request, f'Error al confirmar el pago: {e}')
        return redirect('reserva_fallida_id', solicitud.pk)

def reserva_exitosa(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)

    return render(request, 'veterinaria/pago/reserva_exitosa.html', {'solicitud': solicitud})


def reserva_fallida(request, id=None):
    solicitud = None

    if id:
        solicitud = get_object_or_404(SolicitudCita, id=id)

    return render(request, 'veterinaria/pago/reserva_fallida.html', {'solicitud': solicitud})

