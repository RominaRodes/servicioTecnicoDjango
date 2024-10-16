# Generated by Django 5.0.6 on 2024-10-09 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='dni',
            field=models.CharField(blank=True, max_length=8, null=True, verbose_name='DNI'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='migrated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='codigo_postal',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='condicion_iva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.condicioniva'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='contacto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='cuit',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CUIT'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='domicilio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='localidad',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='razon_social',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefono_alternativo',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='tipo_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.tipocliente'),
        ),
    ]
