# Generated by Django 5.0.6 on 2024-06-24 00:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_alter_presupuesto_repuestos'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesorio',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.categoria'),
        ),
    ]