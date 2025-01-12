from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Repuesto
from .utils import enviar_alerta_stock_critico

@receiver(post_save, sender=Repuesto)
def verificar_stock_critico(sender, instance, **kwargs):
    if instance.stock <= instance.stock_critico and not instance.correo_enviado:
        # Enviar correo solo si no se ha enviado antes
        enviar_alerta_stock_critico(instance)
        instance.correo_enviado = True  # Marcar como enviado
        instance.save()
    elif instance.stock > instance.stock_critico and instance.correo_enviado:
        # Resetear estado si el stock vuelve a ser suficiente
        instance.correo_enviado = False
        instance.save()
