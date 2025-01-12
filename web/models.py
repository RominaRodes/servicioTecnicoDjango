
from django.db import models
from django.utils import timezone
import uuid
from django.core.exceptions import ValidationError
from django.contrib import messages


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
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  
    costo_ultima_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Costo último
    costo_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Costo promedio USD
    stock = models.PositiveIntegerField(default=0)  
    stock_critico = models.PositiveIntegerField(default=1)
    ubicacion = models.CharField(max_length=100, blank=True, default='---')
    correo_enviado = models.BooleanField(default=False)

    def registrar_movimiento_inicial(self):
        """Registra un movimiento inicial al crear un nuevo repuesto."""
        if self.stock > 0:
            costo_inicial = self.costo_ultima_compra or self.precio
            movimiento = MovimientoStockRepuesto.objects.create(
                repuesto=self,
                tipo='entrada',
                cantidad=self.stock,
                costo_unitario=costo_inicial,
                destino='Registro inicial'
            )
            # Actualizar el costo de última compra y costo promedio
            self.costo_ultima_compra = costo_inicial
            self.actualizar_costo_promedio()
            self.save(update_fields=['costo_ultima_compra', 'costo_usd'])

    def descontar_stock(self, cantidad):
        """Descuenta una cantidad del stock actual."""
        if cantidad <= self.stock:
            self.stock -= cantidad
            self.save()
            
        else:
            raise ValidationError(f"No hay suficiente stock para el repuesto: {self.nombre}")



    def aumentar_stock(self, cantidad):
        """Aumenta el stock actual en la cantidad especificada."""
        self.stock += cantidad
        self.save()

    def calcular_costo_promedio(self):
        """Calcula el costo promedio basado en todas las compras."""
        movimientos = self.movimientostockrepuesto_set.filter(tipo='entrada')
        total_costo = sum(mov.cantidad * mov.costo_unitario for mov in movimientos if mov.costo_unitario)
        total_cantidad = sum(mov.cantidad for mov in movimientos)

        return total_costo / total_cantidad if total_cantidad > 0 else 0
    
    def actualizar_costo_promedio(self):
        """Actualiza el costo promedio en el campo costo_usd."""
        self.costo_usd = self.calcular_costo_promedio()
        self.save()

    def verificar_stock_critico(self):
        """Verifica si el stock está en o por debajo del nivel crítico."""
        return self.stock <= self.stock_critico
        # Señal para registrar automáticamente un movimiento de entrada al crear un repuesto
            
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
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Costo por unidad para entradas")
    costo_promedio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Costo promedio al momento del movimiento")  
    fecha = models.DateTimeField(auto_now_add=True)
    destino = models.CharField(max_length=100, blank=True, null=True, help_text="Número de Orden o 'Mostrador' para ventas directas")
    stock_parcial = models.PositiveIntegerField(default=0) 

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Verificar si es un movimiento nuevo

        if is_new:
            # Obtener el último movimiento para calcular el saldo parcial
            ultimo_movimiento = MovimientoStockRepuesto.objects.filter(
                repuesto=self.repuesto
            ).exclude(pk=self.pk).order_by('-fecha', '-id').first()
            
            saldo_anterior = ultimo_movimiento.stock_parcial if ultimo_movimiento else 0

            # Para el movimiento inicial, asignar directamente el stock actual
            if self.destino == 'Registro inicial':
                self.stock_parcial = self.repuesto.stock
            else:
                self.stock_parcial = saldo_anterior + (self.cantidad if self.tipo == 'entrada' else -self.cantidad)

        super().save(*args, **kwargs)  # Guardar el movimiento

        # Evitar duplicar el ajuste de stock para el movimiento inicial
        if is_new and self.destino != 'Registro inicial':
            # Actualizar el stock del repuesto
            if self.tipo == 'entrada':
                self.repuesto.aumentar_stock(self.cantidad)
                if self.costo_unitario:
                    self.repuesto.costo_ultima_compra = self.costo_unitario
                self.repuesto.actualizar_costo_promedio()
            elif self.tipo == 'salida':
                self.repuesto.descontar_stock(self.cantidad)

        # Calcular el costo promedio del movimiento
        if self.destino == 'Registro inicial':
            self.costo_promedio = self.costo_unitario or 0
        else:
            self.costo_promedio = self.repuesto.costo_usd or 0

        # Guardar nuevamente para actualizar el campo costo_promedio
        super().save(update_fields=['costo_promedio'])




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
        if self.presupuesto and self.presupuesto.aprobado:
            for repuesto_presupuesto in self.presupuesto.repuestopresupuesto_set.all():
                repuesto = repuesto_presupuesto.repuesto
                repuesto.descontar_stock(repuesto_presupuesto.cantidad)
                MovimientoStockRepuesto.objects.create(
                    repuesto=repuesto,
                    tipo='salida',
                    cantidad=repuesto_presupuesto.cantidad,
                    destino=f"Orden {self.id}"
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
        if not self.aprobado:
            for repuesto_presupuesto in self.repuestopresupuesto_set.all():
                repuesto = repuesto_presupuesto.repuesto
                cantidad = repuesto_presupuesto.cantidad
                MovimientoStockRepuesto.objects.create(
                    repuesto=repuesto,
                    tipo='salida',
                    cantidad=cantidad,
                    destino=f"Orden {self.orden.id}"
                )
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



