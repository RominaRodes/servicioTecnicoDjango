
from django.db import models
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Categoría")

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return f"{self.nombre}"


        


class SubCategoria(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Subcategoría")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="categorias")

    class Meta:
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del modelo")
    especificaciones = models.CharField(max_length=255, blank=True, null=True,verbose_name="Especificaciones y descripción del modelo")
    manual = models.URLField( blank=True, null=True, verbose_name="URL del manual en formato pdf")
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, related_name="modelos")

    class Meta:
        verbose_name_plural = "Modelos"

    def __str__(self):
        return self.nombre


class SubCategoriaModelo(models.Model):
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subcategoria', 'modelo'], name='unique_subcategoria_modelo')
        ]


class Accesorio(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
            return  f"{self.nombre}"
    
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, default="--")
    telefono = models.CharField(max_length=20, blank=True, default="--")
    email = models.EmailField(blank=True, default="--")

    def __str__(self):
        return self.nombre

class Repuesto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    codigo = models.CharField(max_length=50, default="SIN-CODIGO")
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    costo_ultima_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Costo último
    costo_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Costo promedio USD para cálculo promedio
    cantidad_actual = models.PositiveIntegerField(default=0)  # Control de stock
    stock_critico = models.PositiveIntegerField(default=1)
    ubicacion= models.CharField(max_length=100, blank=True, default='---')

    def descontar_stock(self, cantidad):
        """Descuenta una cantidad del stock actual."""
        if cantidad <= self.cantidad_actual:
            self.cantidad_actual -= cantidad
            self.save()
        else:
            raise ValidationError(f"No hay suficiente stock para el repuesto: {self.nombre}")

    def aumentar_stock(self, cantidad):
        """Aumenta el stock actual en la cantidad especificada."""
        self.cantidad_actual += cantidad
        self.save()

    def __str__(self):
        return f"{self.nombre} - {self.codigo}"

class MovimientoStockRepuesto(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=100, blank=True, null=True, help_text="Número de Orden o 'Mostrador' para ventas directas")
    
    def save(self, *args, **kwargs):
        # Solo permite movimientos de salida con destino vacío si se especifica un destino manualmente.
        if self.tipo == 'salida' and not self.destino:
            raise ValidationError("Debe especificar un destino para las salidas de stock si no es automático.")
        
        # Ajuste del stock según el tipo de movimiento
        if self.tipo == 'salida':
            self.repuesto.descontar_stock(self.cantidad)
        elif self.tipo == 'entrada':
            self.repuesto.aumentar_stock(self.cantidad)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tipo.capitalize()} de {self.cantidad} - {self.repuesto.nombre} ({self.fecha}) - Destino: {self.destino or 'No especificado'}"




class Maquina(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    serie = models.CharField(max_length=100)
    accesorios = models.ManyToManyField(Accesorio, related_name='maquinas', blank=True)
    garantia = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.categoria} {self.subcategoria} {self.modelo}'
    

class CondicionIVA(models.Model):
    CONSUMIDOR_FINAL = 'Consumidor Final'
    INSCRIPTO = 'inscripto'
    MONOTRIBUTISTA = 'monotributista'
    EXENTO = 'exento'

    CONDICION_IVA_CHOICES = [
        (CONSUMIDOR_FINAL, 'Consumidor Final'),
        (INSCRIPTO, 'Inscripto'),
        (MONOTRIBUTISTA, 'Monotributista'),
        (EXENTO, 'Exento'),
    ]

    nombre = models.CharField(max_length=20, choices=CONDICION_IVA_CHOICES, unique=True)

    def __str__(self):
        return self.get_nombre_display()
    
class TipoCliente(models.Model):
    DISTRIBUIDOR = 'distribuidor'
    PROVEEDOR = 'proveedor'
    PARTICULAR = 'particular'

    TIPO_CLIENTE_CHOICES = [
        (DISTRIBUIDOR, 'Distribuidor'),
        (PROVEEDOR, 'Proveedor'),
        (PARTICULAR, 'Particular'),
    ]

    nombre = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, unique=True)

    def __str__(self):
        return self.get_nombre_display()                              

class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True,verbose_name="Nombre o razon socia")
    empresa = models.BooleanField(default=False)
    razon_social = models.CharField(max_length=100, null=True, blank=True, verbose_name="Razon social")
    contacto = models.CharField(max_length=100, null=True, blank=True, verbose_name="Contacto")
    condicion_iva = models.ForeignKey(CondicionIVA, on_delete=models.CASCADE, verbose_name="Condicion IVA")
    cuit = models.CharField(max_length=100, null=True, blank=True, verbose_name="CUIT")
    dni = models.CharField(max_length=8, null=True, blank=True, verbose_name="DNI")
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    domicilio = models.CharField(max_length=200, null=True, blank=True)
    localidad = models.CharField(max_length=45, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    codigo_postal = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    migrated = models.BooleanField(default=False)  #marca los clientes migrados de access 
    
    def clean(self):
        # Saltea las validationes para clientes migrados
        if not self.migrated:
            if self.empresa and not self.cuit:
                raise ValidationError('CUIT es obligatorio para empresas.')
            if not self.empresa and not self.dni:
                raise ValidationError('DNI es obligatorio para particulares.')
    
    def __str__(self):
        return  f"{self.pk} - {self.nombre}"



class OrdenDeReparacion(models.Model):
    ESTADOS = [
        ('ingresada', 'Ingresada'),
        ('presupuestada', 'Presupuestada'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('reparada', 'Reparada'),
        ('entregada', 'Entregada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ingresada')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    notas =  models.TextField(verbose_name="notas con respecto a la maquina", default='---')

    def descontar_stock(self):
        """Descuenta el stock de cada repuesto en el presupuesto y registra el movimiento con el ID de la orden."""
        if hasattr(self, 'presupuesto'):
            for repuesto_presupuesto in self.presupuesto.repuestopresupuesto_set.all():
                repuesto = repuesto_presupuesto.repuesto
                cantidad = repuesto_presupuesto.cantidad

                # Descontar el stock del repuesto
                repuesto.descontar_stock(cantidad)

                # Registrar el movimiento de salida de stock con el ID de la orden como destino
                MovimientoStockRepuesto.objects.create(
                    repuesto=repuesto,
                    tipo='salida',
                    cantidad=cantidad,
                    destino=str(self.id)  # Usa el ID de la orden como destino
                )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not is_new:
            orig = OrdenDeReparacion.objects.get(pk=self.pk)
            orig_estado = orig.estado
        else:
            orig_estado = None
        super().save(*args, **kwargs)  # Guardar la OrdenDeReparacion primero

        # Crear el HistorialEstado si es una nueva instancia de OrdenDeReparacion o el estado ha cambiado
        if is_new or orig_estado != self.estado:
            HistorialEstado.objects.create(orden=self, estado=self.estado)
        
        # Descontar stock solo si el estado cambió a 'reparada'
        if orig_estado != 'reparada' and self.estado == 'reparada':
            self.descontar_stock()

    def __str__(self):
        return f"Orden {self.pk} - {self.cliente.nombre}"

class HistorialEstado(models.Model):
    ESTADOS = OrdenDeReparacion.ESTADOS

    orden = models.ForeignKey(OrdenDeReparacion, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de Orden {self.orden.pk} - {self.estado} en {self.fecha_cambio}"
    
class Presupuesto(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    orden = models.OneToOneField('OrdenDeReparacion', on_delete=models.CASCADE, related_name='presupuesto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    rechazado = models.BooleanField(default=False)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    fecha_rechazo = models.DateTimeField(null=True, blank=True)
    descripcion = models.TextField(verbose_name="Descripcion del presupuesto", default='---')
    nota_interna = models.TextField(verbose_name="Nota interna para técnicos", blank=True, null=True)
    repuestos = models.ManyToManyField(Repuesto, through='RepuestoPresupuesto')
    total_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  


    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


    def __str__(self):
        return f'Presupuesto para Orden {self.orden.id}'
    
    def aprobar(self):
        self.aprobado = True
        self.fecha_aprobacion = timezone.now()
        self.save()

    def rechazar(self):
        self.rechazado = True
        self.fecha_rechazo = timezone.now()
        self.save()
    

    def mail_presupuesto(self):
        pass

class RepuestoPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    @property
    def costo_total_repuesto(self):
        """Calcula el costo total del repuesto en el presupuesto."""
        return self.cantidad * self.repuesto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.repuesto.nombre} para {self.presupuesto}"



