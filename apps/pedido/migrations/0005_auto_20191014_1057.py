# Generated by Django 2.2 on 2019-10-14 13:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0004_auto_20191002_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='precio_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
