from django.core.mail import send_mail
from django.conf import settings

def enviar_alerta_stock_critico(repuesto):
    subject = f"Alerta de stock crítico: {repuesto.nombre}"
    message = (f"El repuesto {repuesto.nombre} ({repuesto.codigo}) ha alcanzado su nivel de stock crítico.\n\n"
               f"Stock actual: {repuesto.stock}\n"
               f"Stock crítico: {repuesto.stock_critico}\n\n"
               "Por favor, reponga este repuesto lo antes posible.")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['rominarodes@gmail.com']  # Cambiar al correo del administrador
    send_mail(subject, message, from_email, recipient_list)

