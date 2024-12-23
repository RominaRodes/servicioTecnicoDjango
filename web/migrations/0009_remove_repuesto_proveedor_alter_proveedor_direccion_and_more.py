# Generated by Django 5.0.6 on 2024-11-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_repuesto_subcategoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repuesto',
            name='proveedor',
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='direccion',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='telefono',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
