from django.shortcuts import redirect, render
from .models import  TipoConsulta, SolicitudCita
from django.contrib import messages
from .forms import SolicitudCitaForm

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
            form.save()
            messages.success(request, 'Cita agendada exitosamente')
            return redirect('index')
    else:
        form = SolicitudCitaForm()
        messages.info(request, 'Complete el formulario para agendar su cita')

    return render(request,'veterinaria/agendar/agendar_form.html',{'form': form})