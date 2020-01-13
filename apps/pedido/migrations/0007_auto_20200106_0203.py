# Generated by Django 2.2 on 2020-01-06 05:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0006_auto_20200106_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregas',
            name='fecha_entrega',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='entregas',
            name='saldo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]