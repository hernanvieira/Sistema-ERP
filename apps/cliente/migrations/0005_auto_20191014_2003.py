# Generated by Django 2.2 on 2019-10-14 23:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0004_auto_20191013_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(99999999)], verbose_name='DNI'),
        ),
    ]
