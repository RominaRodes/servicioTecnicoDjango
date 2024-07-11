from django.contrib import admin
from .models import Categoria, SubCategoria, Modelo, Accesorio, Falla, Repuesto, Maquina, CondicionIVA, Cliente, OrdenDeReparacion, HistorialEstado, Presupuesto


class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id","razon_social", "nombre", "apellido")


admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Modelo)
admin.site.register(Accesorio)
admin.site.register(Falla)
admin.site.register(Repuesto)
admin.site.register(Maquina)
admin.site.register(CondicionIVA)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(OrdenDeReparacion)
admin.site.register(HistorialEstado)
admin.site.register(Presupuesto)

