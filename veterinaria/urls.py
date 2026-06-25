"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import index , agendar_cita , reserva_exitosa, reserva_fallida,iniciar_pago_webpay,retorno_webpay
urlpatterns = [
    path('', index, name='index'),
    path('agendar/', agendar_cita, name='agendar_cita'),

    # WEBPAY
    path('webpay/iniciar/<int:id>/', iniciar_pago_webpay, name='iniciar_pago_webpay'),
    path('webpay/retorno/', retorno_webpay, name='retorno_webpay'),
    path('reserva-exitosa/<int:id>/', reserva_exitosa, name='reserva_exitosa'),
    path('reserva-fallida/', reserva_fallida, name='reserva_fallida'),
    path('reserva-fallida/<int:id>/', reserva_fallida, name='reserva_fallida_id'),
    ]

