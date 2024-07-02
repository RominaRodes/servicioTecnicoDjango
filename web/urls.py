from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import PresupuestoDetailView, EditarPresupuestoView

urlpatterns = [
    path('', views.index, name='index'),
    path('get_ordenes_por_estado/<str:estado>', views.get_ordenes_por_estado, name='get_ordenes_por_estado'),
    path('get_todas_las_ordenes', views.get_todas_las_ordenes, name='get_todas_las_ordenes'),
    path('maquinas', views.maquinas, name='maquinas'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('crearcliente', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='detalle_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.eliminar_cliente, name='eliminar_cliente'),
    path('ordenes/', views.lista_ordenes, name='listado_ordenes'),
    path('crearorden', views.crear_orden, name='crear_orden'),
    path('presupuestar/<int:orden_id>/', views.presupuestar_orden, name='presupuestar_orden'),
    path('presupuesto/<int:pk>/', PresupuestoDetailView.as_view(), name='detalle_presupuesto'),
    path('presupuesto/editar/<int:pk>/', EditarPresupuestoView.as_view(), name='editar_presupuesto'),
    path('aceptar-presupuesto/<uuid:uuid>/', views.aceptar_presupuesto, name='aceptar_presupuesto'),
    path('rechazar-presupuesto/<uuid:uuid>/', views.rechazar_presupuesto, name='rechazar_presupuesto'),
    path('reparar/<int:orden_id>/', views.reparar_orden, name='reparar_orden'),
    path('entregar/<int:orden_id>/', views.entregar_orden, name='entregar_orden'),
    path('ordenes/<int:pk>/', views.OrdenDeReparacionDetailView.as_view(), name='detalle_orden'),
    path('crearorden/categorias/', views.get_categorias, name='get_categorias'),
    path('crearorden/subcategorias/<int:categoria_id>', views.get_subcategorias, name='get_subcategorias'),
    path('crearorden/modelos/<int:subcategoria_id>', views.get_modelos, name='get_modelos'),
    path('crearorden/accesorios/<int:categoria_id>', views.get_accesorios, name='get_accesorios'),
    path('mandar_mail_presupuesto/<int:id_presupuesto>', views.mandar_mail, name='mandar_mail_presupuesto')  
]