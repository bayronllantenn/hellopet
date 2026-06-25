from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Perfil


def login_user(request):

    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            try:
                perfil = Perfil.objects.get(user=user)
                if perfil.rol == 'Recepcionista':
                    return redirect('dashboard_recepcion')
                if perfil.rol == 'Veterinario':
                    return redirect('index_dr')
            except Perfil.DoesNotExist:
                messages.error(request, 'El usuario no tiene un perfil asignado.')
            return redirect('index')
        messages.error(request, 'Usuario o contraseña incorrecta.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('index')