from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recepcion.forms import EditarSolicitudForm, FichaMedicaForm
from veterinaria.models import SolicitudCita, FichaMedica

# Create your views here.
@login_required
def index_recepcion(request):
    return render(request, 'recepcion/index.html')


@login_required
# SOLICITUDES DE CITA , DETALLE SOLICITUD , EDITAR SOLICITUD

def solicitud_citas(request):
    estado = request.GET.get('estado')
    orden = request.GET.get('orden')
    solicitudes = SolicitudCita.objects.all()
    if estado:
        solicitudes = solicitudes.filter(estado=estado)
    if orden == 'recientes':
        solicitudes = solicitudes.order_by('-fecha_creacion')
    else:
        solicitudes = solicitudes.order_by('-fecha_creacion')
    return render(request, 'recepcion/solicitudes/listar_solicitud.html', {'solicitudes': solicitudes,'estado_actual': estado,'orden_actual': orden})

@login_required
def detalle_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)
    return render(request, 'recepcion/solicitudes/detalle_solicitud.html', {'solicitud': solicitud})

@login_required
def editar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)
    if request.method == 'POST':
        form = EditarSolicitudForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()
            return redirect('solicitud_citas_r')
    else:
        form = EditarSolicitudForm(instance=solicitud)
    return render(request, 'recepcion/solicitudes/editar_solicitud.html', {'form': form, 'solicitud': solicitud})



# CREAR FICHA MEDICA , VER FICHA MEDICA , LISTAR FICHAS MEDICAS , EDITAR FICHA MEDICA

@login_required
def crear_ficha(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)
    ficha_existente = FichaMedica.objects.filter(solicitud=solicitud).first()
    if ficha_existente:
        return redirect('ver_ficha_r', id=solicitud.pk)
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.solicitud = solicitud
            ficha.save()
            messages.success(request, 'Ficha medica creada correctamente.')
            return redirect('ver_ficha_r', id=solicitud.pk)
    else:
        form = FichaMedicaForm()
    return render(request, 'recepcion/fichas_medicas/crear_ficha.html', {'form': form, 'solicitud': solicitud, 'action': 'Crear'})

@login_required
def ver_ficha(request, id):
    solicitud = get_object_or_404(SolicitudCita, id=id)
    ficha = get_object_or_404(FichaMedica, solicitud=solicitud)
    return render(request, 'recepcion/fichas_medicas/detalle_ficha.html', {'solicitud': solicitud,'ficha': ficha})


@login_required
def listar_ficha(request):
    fichas = FichaMedica.objects.all().order_by('-fecha_atencion')
    return render(request, 'recepcion/fichas_medicas/listar_ficha.html', {'fichas': fichas})

@login_required
def editar_ficha(request, id):
    ficha = get_object_or_404(FichaMedica, id=id)
    solicitud = ficha.solicitud
    if request.method == 'POST':
        form = FichaMedicaForm(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ficha medica actualizada correctamente.')
            return redirect('ver_ficha_r', id=ficha.solicitud.pk)
    else:
        form = FichaMedicaForm(instance=ficha)
    return render(request, 'recepcion/fichas_medicas/crear_ficha.html', {'form': form, 'ficha': ficha, 'solicitud': solicitud, 'action': 'Editar'})