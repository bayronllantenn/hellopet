from django.contrib import admin
from django.urls import path 
from .views import index_dr,listar_ficha,listar_solicitud,editar_ficha_doctor,detalle_ficha, detalle_cita
urlpatterns = [
    path('' , index_dr , name='index_dr'),
    
    #LISTAR CITAS Y FICHAS
    path('citas/' , listar_solicitud , name='listar_citas'),
    path('fichas/', listar_ficha, name='listar_ficha'),

    #DETALLES DE LAS FICHAS EDITAR , DETALLE , DETALLE CITA
    path('fichas/<int:id>/editar_ficha/', editar_ficha_doctor, name='editar_ficha'),
    path('fichas/<int:id>/detalle_ficha/', detalle_ficha, name='detalle_ficha'),
    path('citas/<int:pk>/detalle_cita/', detalle_cita, name='detalle_cita'),
]
