from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from veterinaria.models import SolicitudCita, FichaMedica
from recepcion.forms import FichaMedicaForm
from django.contrib import messages

# INDEX
@login_required
def index_dr(request):
    return render(request,'doctor/index.html')


# SOLICITAR HORA LOGICA
@login_required
def listar_solicitud(request):
    solicitudes = SolicitudCita.objects.filter(veterinario=request.user,estado='Confirmada').order_by('fecha_hora')
    return render(request,'doctor/citas/listar_cita.html',{'solicitudes': solicitudes})


# FICHA MEDICA LOGICA
@login_required
def listar_ficha(request):
    fichas = FichaMedica.objects.filter(solicitud__veterinario=request.user).order_by('-fecha_atencion')
    return render(request, 'doctor/fichas_medicas/listar_ficha.html', {'fichas': fichas})

@login_required
def editar_ficha_doctor(request, id):

    ficha = get_object_or_404(FichaMedica,id=id,solicitud__veterinario=request.user)
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha medica actualizada correctamente.')
            return redirect('detalle_ficha', id=ficha.pk)
    else:
        form = FichaMedicaForm(instance=ficha)

    return render(request,'doctor/fichas_medicas/editar_ficha.html',{'form': form,'ficha': ficha,'solicitud': ficha.solicitud,'action': 'Editar'})

@login_required
def detalle_ficha(request, id):
    ficha = get_object_or_404(FichaMedica,id=id,solicitud__veterinario=request.user)
    return render( request,'doctor/fichas_medicas/detalle_ficha.html',{'ficha': ficha,'solicitud': ficha.solicitud})

def detalle_cita(request, pk):
    cita = get_object_or_404(SolicitudCita, pk=pk)
    return render(request,"doctor/citas/detalle_cita.html",{"cita": cita})