# Generated by Django 2.2 on 2019-10-13 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_auto_20191013_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1000000), django.core.validators.MaxValueValidator(9999999)], verbose_name='DNI'),
        ),
    ]