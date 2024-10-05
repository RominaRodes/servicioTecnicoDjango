
from django.db import models
from django.utils import timezone
import uuid

class Categoria(models.Model):
    DESTRUCTORA = "Destructoras"
    CONTADORA = "Contadoras"
    CALCULADORA = "Calculadoras"
    ACCESORIOS = "Accesorios para Moviles"
    PROYECTORES = "Proyectores"

    CATEGORIAS = [
        (DESTRUCTORA, "Destructoras de Documento"),
        (CONTADORA, "Contadoras de billetes"),
        (CALCULADORA, "Calculadoras"),
        (ACCESORIOS, "Accesorios para Moviles"),
        (PROYECTORES, "Proyectores"),
    ]

    nombre = models.CharField(max_length=60, choices=CATEGORIAS, verbose_name="Categoría")

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class SubCategoria(models.Model):
    nombre = models.CharField(max_length=60, verbose_name="Subcategoría")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="categorias")

    class Meta:
        verbose_name_plural = "Subcategorías"

    def __str__(self):
        return f"{self.categoria.get_nombre_display()} - {self.nombre}"


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del modelo")
    especificaciones = models.TextField(verbose_name="Especificaciones y descripción del modelo")
    manual = models.URLField(verbose_name="URL del manual en formato pdf")
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


class Falla(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion
    
class Repuesto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Maquina(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.SET_NULL, null=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    serie = models.CharField(max_length=100)
    accesorios = models.ManyToManyField(Accesorio, related_name='maquinas')
    falla = models.ForeignKey(Falla, on_delete=models.SET_NULL, null=True)
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


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del cliente")
    apellido = models.CharField(max_length=100, verbose_name="Apellido del cliente")
    empresa = models.BooleanField(default=False)
    razon_social = models.CharField(max_length=100, verbose_name="Razon Social", null=True, blank=True)
    condicion_iva = models.ForeignKey(CondicionIVA, on_delete=models.CASCADE, verbose_name="Condición IVA")
    cuit= models.CharField(max_length=100, verbose_name="Cuit", null=True, blank=True)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE, default=3, verbose_name="Tipo Cliente")
    domicilio = models.CharField(max_length=200, verbose_name="Domicilio")
    localidad = models.CharField(max_length=45, verbose_name="Localidad")
    codigo_postal = models.CharField(max_length=6, verbose_name="Codigo Postal")
    telefono = models.CharField(max_length=20, verbose_name="Telefono")
    telefono_alternativo = models.CharField(max_length=20, verbose_name="Telefono Alternativo", null=True, blank=True)
    email = models.CharField(max_length=100, verbose_name="Email", unique=True)

    
    def __str__(self):
        return  f"{self.pk} - {self.razon_social or ''} {self.nombre} {self.apellido}"



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

    def __str__(self):
        return f"Orden {self.pk} - {self.cliente.nombre} {self.cliente.apellido}"

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
    total = models.DecimalField(max_digits=10, decimal_places=2)

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




