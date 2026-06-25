from django.contrib import admin
from django.urls import path 
from .views import detalle_solicitud, editar_solicitud, index_recepcion, solicitud_citas , crear_ficha,listar_ficha,ver_ficha ,editar_ficha

urlpatterns = [
    # INICIO
    path('', index_recepcion, name='dashboard_recepcion'),

    # CITAS
    path('solicitudes/', solicitud_citas, name='solicitud_citas_r'),
    path('solicitudes/<int:id>/', detalle_solicitud, name='detalle_solicitud_r'),
    path('solicitudes/<int:id>/editar/', editar_solicitud, name='editar_solicitud_r'),
    
    #FICHAS MEDICAS
    path('fichas/<int:id>/', crear_ficha, name='crear_ficha_r'),
    path('fichas/listar/', listar_ficha, name='listar_ficha_r'),
    path('fichas/detalle_ficha/<int:id>/', ver_ficha, name='ver_ficha_r'),
    path('fichas/<int:id>/editar/', editar_ficha, name='editar_ficha_r'),
]
