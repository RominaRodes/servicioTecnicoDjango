# Generated by Django 5.0.6 on 2024-11-04 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_categoria_nombre_alter_cliente_condicion_iva_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelo',
            name='especificaciones',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Especificaciones y descripción del modelo'),
        ),
        migrations.AlterField(
            model_name='modelo',
            name='manual',
            field=models.URLField(blank=True, null=True, verbose_name='URL del manual en formato pdf'),
        ),
    ]