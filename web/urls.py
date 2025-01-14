from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import PresupuestoDetailView, EditarPresupuestoView, SearchResultsView, BuscarClienteView, BuscarRepuestoView

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('get_ordenes_por_estado/<str:estado>', views.get_ordenes_por_estado, name='get_ordenes_por_estado'),
    path('get_todas_las_ordenes', views.get_todas_las_ordenes, name='get_todas_las_ordenes'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),


    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('crearcliente', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='detalle_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='eliminar_cliente'),
    path('buscar_cliente/', BuscarClienteView.as_view(), name='buscar_cliente_results'),

    path('repuestos/', views.lista_repuestos, name='repuestos'),
    path('repuestos/crear/', views.crear_repuesto, name='crear_repuesto'),
    path('repuestos/editar/<int:pk>/', views.editar_repuesto, name='editar_repuesto'),
    path('repuestos/movimiento_repuestos/<int:pk>/', views. movimientos_repuesto, name='movimientos_repuesto'),
    path('repuestos/registrar_compra/<int:pk>/', views.registrar_compra, name='registrar_compra'),
    path('repuestos/ajustar_stock/<int:pk>/', views.ajustar_stock, name='ajustar_stock'),
    path('buscar_repuesto/', BuscarRepuestoView.as_view(), name='buscar_repuesto_results'),

    path('ordenes/', views.lista_ordenes, name='listado_ordenes'),
    path('crearorden', views.crear_orden, name='crear_orden'),
    path('ordenes/<int:pk>/', views.OrdenDeReparacionDetailView.as_view(), name='detalle_orden'),
    path('crearorden/categorias/', views.get_categorias, name='get_categorias'),
    path('crearorden/subcategorias/<int:categoria_id>', views.get_subcategorias, name='get_subcategorias'),
    path('crearorden/modelos/<int:subcategoria_id>', views.get_modelos, name='get_modelos'),
    path('crearorden/accesorios/<int:categoria_id>', views.get_accesorios, name='get_accesorios'),

    path('presupuestar/<int:orden_id>/', views.presupuestar_orden, name='presupuestar_orden'),
    path('presupuesto/<int:pk>/', PresupuestoDetailView.as_view(), name='detalle_presupuesto'),
    path('presupuesto/editar/<int:pk>/', EditarPresupuestoView.as_view(), name='editar_presupuesto'),
    path('rechazar-presupuesto/<uuid>/', views.rechazar_presupuesto_por_mail, name='rechazar_presupuesto_por_mail'),
    path('confirmar-rechazar-presupuesto/<uuid>/', views.confirmar_rechazar_presupuesto, name='confirmar_rechazar_presupuesto'),
    path('aceptar-presupuesto/<uuid>/', views.aceptar_presupuesto_por_mail, name='aceptar_presupuesto_por_mail'),
    path('confirmar-aceptar-presupuesto/<uuid>/', views.confirmar_aceptar_presupuesto, name='confirmar_aceptar_presupuesto'),
    path('reparar/<int:orden_id>/', views.reparar_orden, name='reparar_orden'),
    path('entregar/<int:orden_id>/', views.entregar_orden, name='entregar_orden'),

    path('mandar_mail_orden/<int:id_orden>', views.mandar_mail_comprobante_entrega, name='mandar_mail_orden'),
    path('mandar_mail_presupuesto/<int:id_presupuesto>', views.mandar_mail, name='mandar_mail_presupuesto'),


]