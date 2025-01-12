from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ClienteForm, DetalleClienteForm, OrdenDeReparacionForm,  PresupuestoForm, MaquinaForm, CrearRepuestoForm, EditarRepuestoForm
from .models import Cliente, OrdenDeReparacion, Maquina, Presupuesto, HistorialEstado, SubCategoria, Modelo, Categoria, Accesorio, Repuesto, RepuestoPresupuesto, MovimientoStockRepuesto
import math 
from django.views.generic import TemplateView, ListView
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.db.models import Sum, F
from django.core.paginator import Paginator
from django.http import JsonResponse
from .pdfs import generar_template_presupuesto
from .pdfs import generar_template_comprobante
from django.utils import timezone
from django.core.mail import EmailMessage
from datetime import timedelta
import logging
from io import BytesIO
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
from django.shortcuts import reverse as django_reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from email.mime.image import MIMEImage
from django.db.models import Q,Case, When, Value, IntegerField
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
logger = logging.getLogger(__name__)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Hola {user}')
            return redirect('index')
        else: 
            messages.error(request, 'Credenciales incorrectas. Intente nuevamente')
            return render(request, 'web/users/login.html', {}) 
    else: 
        return render(request, 'web/users/login.html', {})        

def logout_user(request): 
    logout(request)
    messages.success(request, "Se cerró la sesión correctamente")
    return redirect('login')

@login_required
def index(request):
    estado = request.GET.get('estado', '')
    if estado:
        ordenes = OrdenDeReparacion.objects.filter(estado=estado).order_by('-fecha_ingreso')
    else:
        ordenes = OrdenDeReparacion.objects.all().order_by('-fecha_ingreso')
    
    ordenes_info = []
    for orden in ordenes:
        ultimo_historial = HistorialEstado.objects.filter(orden=orden).latest('fecha_cambio')
        accesorios = orden.maquina.accesorios.all()
        presupuesto = Presupuesto.objects.filter(orden=orden.id).first()
        if presupuesto:
            presupuesto_uuid = presupuesto.uuid
            presupuesto_id = presupuesto.id
        else:
            presupuesto_uuid = None
            presupuesto_id = None

        orden_info = {
            'orden': orden,
            'cliente': orden.cliente,
            'maquina': orden.maquina,
            'accesorios': accesorios,
            'ultimo_estado': ultimo_historial.estado,
            'fecha_ultimo_estado': ultimo_historial.fecha_cambio,
            'presupuesto_uuid': presupuesto_uuid,
            'presupuesto_id': presupuesto_id
        }
        ordenes_info.append(orden_info)


    paginator = Paginator(ordenes_info, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_ordenes': OrdenDeReparacion.objects.count(),
        'total_ingresadas': OrdenDeReparacion.objects.filter(estado='ingresada').count(),
        'total_aceptadas': OrdenDeReparacion.objects.filter(estado='aceptada').count(),
        'total_reparadas': OrdenDeReparacion.objects.filter(Q(estado='reparada') | Q(estado='rechazada')).count(),
        'total_entregadas': OrdenDeReparacion.objects.filter(estado='entregada').count(),
        'page_obj': page_obj,
    }
  
    return render(request, 'web/index.html', context)

@login_required
def get_todas_las_ordenes(request):
    ordenes_qs = OrdenDeReparacion.objects.all().order_by('-fecha_ingreso')
    ordenes_info = []

    for orden in ordenes_qs:
        ultimo_historial = HistorialEstado.objects.filter(orden=orden).latest('fecha_cambio')
        accesorios = orden.maquina.accesorios.all()
        presupuesto = Presupuesto.objects.filter(orden=orden).first()
        presupuesto_uuid = presupuesto.uuid if presupuesto else None
        presupuesto_id = presupuesto.id if presupuesto else None

        orden_info = {
            'orden': {
                'id': orden.id,
                'cliente': {
                    'id': orden.cliente.id,
                    'nombre': orden.cliente.nombre,
                    'empresa': orden.cliente.empresa,
                    'razon_social': orden.cliente.razon_social
                },
                'maquina': {
                    'id': orden.maquina.id,
                    'categoria': orden.maquina.categoria.nombre,
                    'subcategoria': orden.maquina.subcategoria.nombre,
                    'modelo': orden.maquina.modelo.nombre,
                    'serie': orden.maquina.serie,
                },
                'estado': orden.estado,
                'fecha_ingreso': orden.fecha_ingreso,
                'notas': orden.notas,
            },
            'accesorios': list(accesorios.values('nombre')),
            'ultimo_estado': ultimo_historial.estado,
            'fecha_ultimo_estado': ultimo_historial.fecha_cambio,
            'presupuesto_id': presupuesto_id,
            'presupuesto_uuid': presupuesto_uuid
        }
        ordenes_info.append(orden_info)

    data = {'message': 'Success', 'ordenes': ordenes_info}
    return JsonResponse(data, safe=False)


def get_ordenes_por_estado(request, estado):
    ordenes_qs = OrdenDeReparacion.objects.filter(estado=estado).order_by('-fecha_ingreso')
    ordenes_info = []

    for orden in ordenes_qs:
        ultimo_historial = HistorialEstado.objects.filter(orden=orden).latest('fecha_cambio')
        accesorios = orden.maquina.accesorios.all()
        presupuesto = Presupuesto.objects.filter(orden=orden).first()
        presupuesto_id = presupuesto.id if presupuesto else None
        presupuesto_uuid = presupuesto.uuid if presupuesto else None

        orden_info = {
            'orden': {
                'id': orden.id,
                'cliente': {
                    'id': orden.cliente.id,
                    'nombre': orden.cliente.nombre,
                    'empresa': orden.cliente.empresa,
                    'razon_social': orden.cliente.razon_social
                },
                'maquina': {
                    'id': orden.maquina.id,
                    'categoria': orden.maquina.categoria.nombre,
                    'subcategoria': orden.maquina.subcategoria.nombre,
                    'modelo': orden.maquina.modelo.nombre,
                    'serie': orden.maquina.serie,
                },
                'estado': orden.estado,
                'fecha_ingreso': orden.fecha_ingreso,
                'notas': orden.notas,
            },
            'accesorios': list(accesorios.values('nombre')),
            'ultimo_estado': ultimo_historial.estado,
            'fecha_ultimo_estado': ultimo_historial.fecha_cambio,
            'presupuesto_id': presupuesto_id,
            'presupuesto_uuid': presupuesto_uuid,
        }
        ordenes_info.append(orden_info)

    data = {'message': 'Success', 'ordenes': ordenes_info}
    return JsonResponse(data, safe=False)


class SearchResultsView(LoginRequiredMixin, ListView):
    model = OrdenDeReparacion
    template_name = 'web/search_results.html'

    def get_queryset(self):  
        query = self.request.GET.get("q")
        if not query:
            return OrdenDeReparacion.objects.none()

        object_list = OrdenDeReparacion.objects.filter(
            Q(id__icontains=query) |
            Q(maquina__serie__icontains=query) |
            Q(maquina__categoria__nombre__icontains=query) |
            Q(estado__icontains=query) |
            Q(cliente__id__icontains=query) |
            Q(cliente__razon_social__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__contacto__icontains=query) |
            Q(cliente__dni__icontains=query) |
            Q(cliente__cuit__icontains=query)
        )

        return object_list


class BuscarClienteView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'web/buscar_cliente_results.html'
    paginate_by = 15  # Pagina automáticamente

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if query.isdigit():  # Si la consulta es numérica
                return Cliente.objects.filter(
                    Q(id__icontains=query) |
                    Q(cuit__icontains=query) |
                    Q(dni__icontains=query) |
                    Q(telefono__icontains=query)
                ).order_by('id')
            else:  # Si la consulta contiene letras
                return Cliente.objects.filter(
                    Q(nombre__icontains=query) |
                    Q(contacto__icontains=query) |
                    Q(email__icontains=query)
                ).annotate(
                    search_priority=Case(
                        When(nombre__icontains=query, then=Value(1)),
                        When(contacto__icontains=query, then=Value(2)),
                        When(email__icontains=query, then=Value(3)),
                        default=Value(4),
                        output_field=IntegerField(),
                    )
                ).order_by('search_priority', 'id')
        return Cliente.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context
    
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('-id')

    paginator = Paginator(clientes, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'web/lista_clientes.html', {'page_obj': page_obj,'clientes': clientes })

@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'El cliente id: {cliente} fue creado con éxito')
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    total_fields = len(form.fields)
    half = math.ceil(total_fields / 2)
    
    return render(request, 'web/crear_cliente.html', {'form': form, 'half': half})

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'web/detalle_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordenes'] = OrdenDeReparacion.objects.filter(cliente=self.object)
        return context

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'El cliente id: {cliente} fue editado con éxito')
            return redirect('detalle_cliente', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)

    total_fields = len(form.fields)
    half = math.ceil(total_fields / 2)

    return render(request, 'web/editar_cliente.html', {'form': form, 'half': half, 'cliente_id': cliente.id })


class ClienteDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Cliente
    success_url = reverse_lazy('lista_clientes')  
    success_message = "El cliente fue eliminado con éxito."

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Cliente, id=id_)


@login_required
def crear_orden(request):
    if request.method == 'POST':
        orden_form = OrdenDeReparacionForm(request.POST)
        maquina_form = MaquinaForm(request.POST)

        if orden_form.is_valid() and maquina_form.is_valid():
            maquina = maquina_form.save()
            orden = orden_form.save(commit=False)
            orden.maquina = maquina
            orden.save()
            messages.success(request, f'La {orden} fue ingresada con éxito')
            return redirect('listado_ordenes')  
    else:
        orden_form = OrdenDeReparacionForm()
        maquina_form = MaquinaForm()

    return render(request, 'web/crear_orden.html', {
        'orden_form': orden_form,
        'maquina_form': maquina_form,
    })

@login_required
def lista_ordenes(request):
    estado = request.GET.get('estado', '')
    if estado:
        ordenes = OrdenDeReparacion.objects.filter(estado=estado).order_by('-fecha_ingreso')
    else:
        ordenes = OrdenDeReparacion.objects.all().order_by('-fecha_ingreso')
    
    ordenes_info = []
    for orden in ordenes:
        ultimo_historial = HistorialEstado.objects.filter(orden=orden).latest('fecha_cambio')
        accesorios = orden.maquina.accesorios.all()
        presupuesto = Presupuesto.objects.filter(orden=orden.id).first()
        if presupuesto:
            presupuesto_uuid = presupuesto.uuid
            presupuesto_id = presupuesto.id
        else:
            presupuesto_uuid = None
            presupuesto_id = None

        orden_info = {
            'orden': orden,
            'cliente': orden.cliente,
            'maquina': orden.maquina,
            'accesorios': accesorios,
            'ultimo_estado': ultimo_historial.estado,
            'fecha_ultimo_estado': ultimo_historial.fecha_cambio,
            'presupuesto_uuid': presupuesto_uuid,
            'presupuesto_id': presupuesto_id
        }
    
        ordenes_info.append(orden_info)
    
    context = {
    'ordenes_info': ordenes_info,
    }
    return render(request, 'web/lista_ordenes.html', context)

    
@login_required
def lista_repuestos(request):
    repuestos = Repuesto.objects.all().order_by('-id')

    paginator = Paginator(repuestos, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'web/lista_repuestos.html', {'page_obj': page_obj,'repuestos': repuestos })

@staff_member_required
def crear_repuesto(request):
    if request.method == 'POST':
        form = CrearRepuestoForm(request.POST)
        if form.is_valid():
            repuesto = form.save()
            repuesto.registrar_movimiento_inicial()  # Registrar el movimiento inicial
            messages.success(request, 'Repuesto creado con éxito.')
            return redirect('repuestos') 

    else:
        form = CrearRepuestoForm()

    return render(request, 'web/crear_repuesto.html', {'form': form})
    

@staff_member_required
def editar_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == "POST":
        form = EditarRepuestoForm(request.POST, instance=repuesto)
        if form.is_valid():
            form.save()
            messages.success(request, "Repuesto actualizado correctamente.")
            return redirect('movimientos_repuesto', pk=repuesto.id)

    else:
        form = EditarRepuestoForm(instance=repuesto)
    return render(request, 'web/editar_repuesto.html', {'form': form})

@staff_member_required
def ajustar_stock(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    
    if request.method == "POST":
        try:
            nueva_cantidad = int(request.POST.get('nueva_cantidad'))
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa.")
        except (ValueError, TypeError):
            messages.error(request, "Ingrese una cantidad válida. Debe ser un número entero no negativo.")
            return render(request, 'web/ajustar_stock.html', {'repuesto': repuesto})

        diferencia = nueva_cantidad - repuesto.stock

        if diferencia == 0:
            messages.info(request, "No hubo cambios en el stock.")
            return redirect('movimientos_repuesto', pk=repuesto.id)

        tipo_movimiento = 'entrada' if diferencia > 0 else 'salida'

        # Registrar el movimiento
        MovimientoStockRepuesto.objects.create(
            repuesto=repuesto,
            tipo=tipo_movimiento,
            cantidad=abs(diferencia),
            destino='Ajuste manual',
            costo_unitario=repuesto.costo_ultima_compra if tipo_movimiento == 'entrada' else None
        )

        # Mensajes según el estado del stock
        if repuesto.verificar_stock_critico():
            messages.warning(request, f"El stock de {repuesto.nombre} está en nivel crítico ({repuesto.stock} unidades).")
        else:
            messages.success(request, f"Stock actualizado a {nueva_cantidad}.")

        return redirect('movimientos_repuesto', pk=repuesto.id)

    return render(request, 'web/ajustar_stock.html', {'repuesto': repuesto})

@staff_member_required
def registrar_compra(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad'))
        costo_unitario = float(request.POST.get('costo_unitario'))

        movimiento = MovimientoStockRepuesto.objects.create(
            repuesto=repuesto,
            tipo='entrada',
            cantidad=cantidad,
            costo_unitario=costo_unitario,
            destino='Compra'
        )
        movimiento.save()
        # Depuración
        print(f"Stock después de registrar la compra: {repuesto.stock}")
        print(f"Costo promedio actualizado: {repuesto.costo_usd}")

        messages.success(request, f"Compra registrada: {cantidad} unidades de '{repuesto.nombre}' a {costo_unitario} cada una.")
        return redirect('movimientos_repuesto', pk=repuesto.id)
    
    return render(request, 'web/registrar_compra.html', {'repuesto': repuesto})


class BuscarRepuestoView(LoginRequiredMixin, ListView):
    model = Repuesto
    template_name = 'web/buscar_repuesto_results.html'
    paginate_by = 15  
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = Repuesto.objects.filter(
                Q(nombre__icontains=query) |
                Q(codigo__icontains=query) |
                Q(categoria__nombre__icontains=query)
            ).annotate(
                search_priority=Case(
                    When(nombre__icontains=query, then=Value(1)),
                    When(categoria__nombre__icontains=query, then=Value(2)),
                    When(codigo__icontains=query, then=Value(3)),
                    default=Value(4),
                    output_field=IntegerField(),
                )
            ).order_by('search_priority', 'id')
        else:
            object_list = Repuesto.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("q")
        return context


@staff_member_required
def movimientos_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    movimientos = MovimientoStockRepuesto.objects.filter(repuesto=repuesto).order_by('-fecha')
    
    paginator = Paginator(movimientos, 15)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if movimientos.exists():
        ultimo_movimiento = movimientos.order_by('fecha', 'id').last()

        if ultimo_movimiento.stock_parcial != repuesto.stock:
            messages.warning(
                request,
                f"Inconsistencia detectada: El stock actual ({repuesto.stock}) no coincide con el stock parcial del último movimiento ({ultimo_movimiento.stock_parcial})."
            )

    return render(request, 'web/movimientos_repuesto.html', {
        'repuesto': repuesto,
        'page_obj': page_obj,
        'movimientos': movimientos,
    })

@staff_member_required
def presupuestar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeReparacion, pk=orden_id)

    # Verificar si ya existe un presupuesto para esta orden
    if hasattr(orden, 'presupuesto'):
        messages.error(request, "Ya existe un presupuesto para esta orden.")
        return redirect('detalle_presupuesto', pk=orden.presupuesto.pk)

    if request.method == "POST":
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.orden = orden
            presupuesto.save()
            
            # Procesar los repuestos y cantidades
            repuestos_ids = request.POST.getlist('repuesto_id')
            cantidades = request.POST.getlist('cantidad')

            for repuesto_id, cantidad in zip(repuestos_ids, cantidades):
                repuesto = Repuesto.objects.get(id=repuesto_id)
                cantidad = int(cantidad)
                
                # Validar stock suficiente
                if repuesto.stock < cantidad:
                    messages.error(request, f"No hay suficiente stock para el repuesto {repuesto.nombre}.")
                    presupuesto.delete() 
                    return redirect('presupuestar_orden', orden_id=orden.id)
                
                RepuestoPresupuesto.objects.create(
                    presupuesto=presupuesto,
                    repuesto=repuesto,
                    cantidad=cantidad
                )

            orden.estado = 'presupuestada'
            orden.save()

            messages.success(request, 'Presupuesto creado con éxito.')
            print(f"Presupuesto ID: {presupuesto.id}")  

            return redirect('detalle_presupuesto', pk=presupuesto.id)
    else:
        form = PresupuestoForm()
    
    # Filtrar solo repuestos con stock disponible
    repuestos = Repuesto.objects.filter(stock__gt=0)
    return render(request, 'web/crear_presupuesto.html', {
        'form': form,
        'orden': orden,
        'repuestos': repuestos
    })

@login_required
def aceptar_presupuesto_por_mail(request, uuid):
    presupuesto = get_object_or_404(Presupuesto, uuid=uuid)
    if timezone.now() > presupuesto.fecha_creacion + timedelta(days=30):
        return HttpResponseBadRequest("El enlace ha caducado.")
    
    presupuesto.aprobar()  # Aprobar el presupuesto y generar movimientos

    # Verificar si algún repuesto está en nivel crítico
    repuestos_criticos = []
    for repuesto_presupuesto in presupuesto.repuestopresupuesto_set.all():
        repuesto = repuesto_presupuesto.repuesto
        if repuesto.verificar_stock_critico():  # Llama al método que verifica el stock crítico
            repuestos_criticos.append(repuesto.nombre)
    
    # Mostrar mensaje si hay repuestos críticos
    if repuestos_criticos:
        repuestos_list = ", ".join(repuestos_criticos)
        messages.warning(
            request,
            f"Los siguientes repuestos alcanzaron el nivel crítico de stock: {repuestos_list}."
        )

    # Actualizar estado de la orden
    presupuesto.orden.estado = 'aceptada'
    presupuesto.orden.save()

    messages.success(request, 'El presupuesto fue aceptado con éxito.')
    return redirect('listado_ordenes')


@login_required
def rechazar_presupuesto_por_mail(request, uuid):
    presupuesto = get_object_or_404(Presupuesto, uuid=uuid)
    if timezone.now() > presupuesto.fecha_creacion + timedelta(days=30):
        return HttpResponseBadRequest("El enlace ha caducado.")
    presupuesto.rechazar()
    presupuesto.orden.estado = 'rechazada'
    presupuesto.orden.save()
    messages.success(request, 'El presupuesto fue rechazado con éxito')
    return redirect('listado_ordenes')

@login_required
def confirmar_aceptar_presupuesto(request, uuid):
    presupuesto = get_object_or_404(Presupuesto, uuid=uuid)
    aceptar_url = reverse('aceptar_presupuesto_por_mail', args=[uuid])
    aceptar_button_html = f'<a href="{aceptar_url}" class="btn btn-primary">Aceptar</a>'
    mensaje = mark_safe(f'¿Está seguro que desea aceptar el presupuesto de la orden n.º {presupuesto.orden}?   {aceptar_button_html}')

    messages.success(request, mensaje)
    return redirect('listado_ordenes')

@login_required
def confirmar_rechazar_presupuesto(request, uuid):
    presupuesto = get_object_or_404(Presupuesto, uuid=uuid)
    rechazar_url = reverse('rechazar_presupuesto_por_mail', args=[uuid])
    rechazar_button_html = f'<a href="{rechazar_url}" class="btn btn-danger">Rechazar</a>'
    mensaje = mark_safe(f'¿Está seguro que desea rechazar el presupuesto de la orden n.º {presupuesto.orden}?   {rechazar_button_html}')
    messages.success(request, mensaje)
    return redirect('listado_ordenes')

@login_required
def reparar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeReparacion, id=orden_id)
    orden.estado = 'reparada'
    orden.save()
    return redirect('listado_ordenes')

@login_required
def entregar_orden(request, orden_id):
    orden = get_object_or_404(OrdenDeReparacion, id=orden_id)
    orden.estado = 'entregada'
    orden.save()
    return redirect('listado_ordenes')

class EditarPresupuestoView(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'web/editar_presupuesto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        presupuesto = self.object

        # Repuestos asociados al presupuesto con subtotales
        repuestos_presupuestos = RepuestoPresupuesto.objects.filter(presupuesto=presupuesto)
        repuestos_con_subtotales = [
            {
                'repuesto': rp.repuesto,
                'cantidad': rp.cantidad,
                'subtotal': rp.cantidad * rp.repuesto.precio
            } for rp in repuestos_presupuestos
        ]

        # Repuestos disponibles con stock > 0
        repuestos_disponibles = Repuesto.objects.filter(stock__gt=0)

        context['repuestos_presupuestos'] = repuestos_con_subtotales
        context['repuestos'] = repuestos_disponibles
        return context

    def form_valid(self, form):
        presupuesto = form.save()

        # Obtener los repuestos y cantidades desde el formulario
        repuestos_ids = self.request.POST.getlist('repuesto_id')
        cantidades = self.request.POST.getlist('cantidad')

        # Validar el stock y manejar los repuestos
        for repuesto_id, cantidad in zip(repuestos_ids, cantidades):
            repuesto = Repuesto.objects.get(id=repuesto_id)
            cantidad = int(cantidad)
            repuesto_presupuesto = RepuestoPresupuesto.objects.filter(
                presupuesto=presupuesto, repuesto=repuesto).first()
            cantidad_anterior = repuesto_presupuesto.cantidad if repuesto_presupuesto else 0
            stock_disponible = repuesto.stock + cantidad_anterior

            if cantidad > stock_disponible:
                messages.error(
                    self.request,
                    f"No hay suficiente stock para el repuesto {repuesto.nombre}. Stock disponible: {stock_disponible}."
                )
                return self.form_invalid(form)

        # Eliminar los repuestos existentes
        RepuestoPresupuesto.objects.filter(presupuesto=presupuesto).delete()

        # Guardar los repuestos nuevos
        for repuesto_id, cantidad in zip(repuestos_ids, cantidades):
            repuesto = Repuesto.objects.get(id=repuesto_id)
            RepuestoPresupuesto.objects.create(
                presupuesto=presupuesto,
                repuesto=repuesto,
                cantidad=int(cantidad)
            )

        messages.success(self.request, 'Presupuesto actualizado con éxito.')
        return redirect('detalle_presupuesto', pk=presupuesto.pk)

    def get_success_url(self):
        return reverse_lazy('detalle_presupuesto', kwargs={'pk': self.object.pk})


class OrdenDeReparacionDetailView(LoginRequiredMixin, DetailView):
    model = OrdenDeReparacion
    template_name = 'web/detalle_orden.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historial'] = HistorialEstado.objects.filter(orden=self.object).order_by('-fecha_cambio')
        context['ultimo_historial_estado'] = context['historial'].filter(estado=self.object.estado).first()
        context['estados'] = ["ingresada", "presupuestada", "aceptada", "rechazada", "reparada", "entregada"]
        presupuesto = Presupuesto.objects.filter(orden=self.object).first()
        context['presupuesto'] = presupuesto
        context['accesorios'] = self.object.maquina.accesorios.all()
        if presupuesto:
            context['presupuesto'] = presupuesto
            context['repuestos'] = RepuestoPresupuesto.objects.filter(presupuesto=presupuesto)
        else:
            context['presupuesto'] = None
            context['repuestos'] = None
        return context


class PresupuestoDetailView(LoginRequiredMixin, DetailView):
    model = Presupuesto
    template_name = 'web/detalle_presupuesto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.object.orden
        context['historial'] = HistorialEstado.objects.filter(orden=orden).order_by('-fecha_cambio')
        context['ultimo_historial_estado'] = context['historial'].filter(estado=orden.estado).first()
        context['estados'] = ["ingresada", "presupuestada", "aceptada", "rechazada", "reparada", "entregada"]
        context['cliente'] = orden.cliente
        context['maquina'] = orden.maquina
        context['orden'] = orden
        context['accesorios'] = orden.maquina.accesorios.all()
        context['total'] = self.object.total_estimado
        context['repuestos'] = RepuestoPresupuesto.objects.filter(presupuesto=self.object)  
        context['total_repuestos'] = RepuestoPresupuesto.objects.filter(presupuesto=self.object) \
            .annotate(subtotal=F('cantidad') * F('repuesto__precio')) \
            .aggregate(total=Sum('subtotal'))['total'] or 0

        return context

@login_required
def get_categorias(_request):
    categorias=list(Categoria.objects.values())

    if(len(categorias)>0):
        data={'message':'Success', 'categorias': categorias}
    else:
        data={'message': "Categorias no encontradas"} 
    return JsonResponse(data)

@login_required
def get_subcategorias(_request,categoria_id):
    subcategorias = list(SubCategoria.objects.filter(categoria=categoria_id).values())
    if(len(subcategorias)>0):
        data={'message':'Success', 'subcategorias': subcategorias}
    else:
        data={'message': "Subcategoria no encontrada"} 

    return JsonResponse(data)

@login_required
def get_modelos(_request, subcategoria_id):
    modelos = list(Modelo.objects.filter(subcategoria=subcategoria_id).values())
    if(len(modelos)>0):
        data={'message':'Success', 'modelos': modelos}
    else:
        data={'message': "Modelos no encontrados"} 

    return JsonResponse(data)

@login_required
def get_accesorios(request, categoria_id):
    accesorios_categoria = list(Accesorio.objects.filter(categoria=categoria_id).values())
    accesorios_generales = list(Accesorio.objects.filter(categoria__isnull=True).values())
    
    accesorios = accesorios_categoria + accesorios_generales
    
    if accesorios:
        data = {'message': 'Success', 'accesorios': accesorios}
    else:
        data = {'message': 'Accesorios no encontrados'}

    return JsonResponse(data)

@login_required
@api_view(['GET'])
def mandar_mail(request,id_presupuesto):
    presupuesto = get_object_or_404(Presupuesto, pk=id_presupuesto)
    orden = presupuesto.orden
    accesorios = orden.maquina.accesorios.all()
    accesorios_list = list(accesorios[:4])  # Limitar a 4 accesorios
    accesorios_dict = {
        'equipo_accesorio1': accesorios_list[0] if len(accesorios_list) > 0 else 'No posee accesorios',
        'equipo_accesorio2': accesorios_list[1] if len(accesorios_list) > 1 else '',
        'equipo_accesorio3': accesorios_list[2] if len(accesorios_list) > 2 else '',
        'equipo_accesorio4': accesorios_list[3] if len(accesorios_list) > 3 else ''
    }
    repuestos = RepuestoPresupuesto.objects.filter(presupuesto=presupuesto)
    repuestos_data = [{
        'codigo': repuesto.repuesto.codigo,
        'nombre': repuesto.repuesto.nombre,
        'cantidad': repuesto.cantidad,
        'precio_unitario': repuesto.repuesto.precio,
        'subtotal': repuesto.cantidad * repuesto.repuesto.precio,
    } for repuesto in repuestos]


    datos = {
        'cliente_nombre': f'{orden.cliente.nombre}',
        'cliente_telefono': orden.cliente.telefono,
        'cliente_email': orden.cliente.email,
        'presupuesto_numero': presupuesto.id,
        'presupuesto_fecha': timezone.now().strftime('%Y-%m-%d'),
        'ingreso_fecha': orden.fecha_ingreso.strftime('%Y-%m-%d'),
        'equipo_categoria': orden.maquina.categoria,
        'equipo_subcategoria': orden.maquina.subcategoria,
        'equipo_modelo': orden.maquina.modelo,
        'equipo_numero_serie': orden.maquina.serie,
        'equipo_garantia': 'Posee' if orden.maquina.garantia else 'No posee',
        'equipo_notas': orden.notas,
        'equipo_insumos': 'Ninguno',  # Agregar este dato para que se incluya
        'presupuesto_descripcion': presupuesto.descripcion,
        'presupuesto_total': presupuesto.total_estimado,
        **accesorios_dict,
        'repuestos': repuestos_data,
    }

    # Generar el PDF en memoria
    pdf_buffer = BytesIO()
    generar_template_presupuesto(pdf_buffer, datos)
    pdf_buffer.seek(0)  

    try:
        uuid = presupuesto.uuid
        aceptar_url = request.build_absolute_uri(reverse('aceptar_presupuesto_por_mail', kwargs={'uuid': uuid}))
        rechazar_url = request.build_absolute_uri(reverse('rechazar_presupuesto_por_mail', kwargs={'uuid': uuid}))
        if orden.cliente.empresa:
            cliente =  f'{orden.cliente.nombre}-{orden.cliente.razon_social}'
        else:
            cliente = f'{orden.cliente.nombre}'
        
        subject= 'Presupuesto - Orden de Reparacion'
        to_mail = orden.cliente.email
        context ={
            'cliente': cliente,
            'aceptar_url': aceptar_url,
            'rechazar_url': rechazar_url,
            'orden_id': orden.id,
            'logo_cid': 'logo_image',
            'imagen_cid': 'example_image'
        }

        html_message = render_to_string('web/emails/presupuesto-email.html', context)
        plain_message= strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=subject,
            body= plain_message,
            from_email=None,
            to=[to_mail],
        )
        message.attach_alternative(html_message, "text/html")

        # crea el nombre del pdf y luego lo adjunta
        if orden.cliente.empresa:
            nombre_pdf = f'{orden.cliente.razon_social.upper()}_presupuesto.pdf'
        else:
            nombre_pdf = f'{orden.cliente.nombre.upper()}_presupuesto.pdf'

        message.attach(nombre_pdf, pdf_buffer.getvalue(), 'application/pdf')

        # Adjuntar imágen logo e imagen cuerpo mial  y agrega Content-ID
        logo_path = settings.STATICFILES_DIRS[0] / 'web/img/LogoUnitronic.png'
        imagen_path = settings.STATICFILES_DIRS[0] / 'web/img/65bc9a46-7405-44fd-8dc1-c779fe5b831d.png'


        with open(logo_path, 'rb') as logo_file:
            logo = MIMEImage(logo_file.read())
            logo.add_header('Content-ID', '<logo_image>')
            message.attach(logo)

        with open(imagen_path, 'rb') as imagen_file:
            imagen = MIMEImage(imagen_file.read())
            imagen.add_header('Content-ID', '<example_image>')
            message.attach(imagen)

        message.send()
        messages.success(request, f'El presupuesto de la orden nro. {orden.id} fue enviado con éxito')
        return redirect('index')  

    except Exception as e:
        logger.error(f'Error al enviar correo electrónico: {str(e)}')
        return Response({"message": f'Error al enviar correo electrónico: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    
@login_required   
@api_view(['GET'])
def mandar_mail_comprobante_entrega(request,id_orden):
    orden = get_object_or_404(OrdenDeReparacion, pk=id_orden)
    accesorios = orden.maquina.accesorios.all()
    accesorios_list = list(accesorios[:4])  # Limitar a 4 accesorios
    accesorios_dict = {
        'equipo_accesorio1': accesorios_list[0] if len(accesorios_list) > 0 else 'No posee accesorios',
        'equipo_accesorio2': accesorios_list[1] if len(accesorios_list) > 1 else '',
        'equipo_accesorio3': accesorios_list[2] if len(accesorios_list) > 2 else '',
        'equipo_accesorio4': accesorios_list[3] if len(accesorios_list) > 3 else ''
    }

    datos = {
        'cliente_nombre': f'{orden.cliente.nombre}',
        'cliente_telefono': orden.cliente.telefono,
        'cliente_email': orden.cliente.email,
        'orden_numero': orden.id,
        'ingreso_fecha': orden.fecha_ingreso.strftime('%Y-%m-%d'),
        'equipo_categoria': orden.maquina.categoria,
        'equipo_subcategoria': orden.maquina.subcategoria,
        'equipo_modelo': orden.maquina.modelo,
        'equipo_numero_serie': orden.maquina.serie,
        'equipo_garantia': 'Posee' if orden.maquina.garantia else 'No posee',
        'equipo_notas': orden.notas,
        'equipo_insumos': 'Ninguno',  # Agregar este dato para que se incluya
        **accesorios_dict
    }

    # Generar el PDF en memoria
    pdf_buffer = BytesIO()
    generar_template_comprobante(pdf_buffer, datos)
    pdf_buffer.seek(0)  # Volver al principio del archivo para poder leerlo

    try:
        if orden.cliente.empresa:
            cliente =  f'{orden.cliente.nombre}-{orden.cliente.razon_social}'
        else:
            cliente = f'{orden.cliente.nombre}'
        
        subject= 'Comprobante de entrega - Orden de Reparacion'
        to_mail = orden.cliente.email
        context ={
            'cliente': cliente,
            'orden_id': orden.id,
            'logo_cid': 'logo_image',
            'imagen_cid': 'example_image'
        }

        html_message = render_to_string('web/emails/comprobante-email.html', context)
        plain_message= strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject=subject,
            body= plain_message,
            from_email=None,
            to=[to_mail],
        )
        message.attach_alternative(html_message, "text/html")

        # crea el nombre del pdf y luego lo adjunta
        if orden.cliente.empresa:
            nombre_pdf = f'{orden.cliente.razon_social.upper()}_ordenReparacion.pdf'
        else:
            nombre_pdf = f'{orden.cliente.nombre.upper()}_ordenReparacion.pdf'

        message.attach(nombre_pdf, pdf_buffer.getvalue(), 'application/pdf')

        # Adjuntar imágen logo e imagen cuerpo mial  y agrega Content-ID
        logo_path = settings.STATICFILES_DIRS[0] / 'web/img/LogoUnitronic.png'
        imagen_path = settings.STATICFILES_DIRS[0] / 'web/img/65bc9a46-7405-44fd-8dc1-c779fe5b831d.png'


        with open(logo_path, 'rb') as logo_file:
            logo = MIMEImage(logo_file.read())
            logo.add_header('Content-ID', '<logo_image>')
            message.attach(logo)

        with open(imagen_path, 'rb') as imagen_file:
            imagen = MIMEImage(imagen_file.read())
            imagen.add_header('Content-ID', '<example_image>')
            message.attach(imagen)

        message.send()
        messages.success(request, f'El email de la orden se reparacion numero {orden.id} fue enviado con éxito')
        return redirect('index')  

    except Exception as e:
        logger.error(f'Error al enviar correo electrónico: {str(e)}')
        return Response({"message": f'Error al enviar correo electrónico: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    