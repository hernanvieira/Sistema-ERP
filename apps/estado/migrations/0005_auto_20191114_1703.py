# Generated by Django 2.2 on 2019-11-14 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estado', '0004_auto_20191114_1512'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='estado_pedido',
            options={'get_latest_by': 'fecha', 'ordering': ['fecha'], 'verbose_name': 'Estado_pedido', 'verbose_name_plural': 'Estados_pedido'},
        ),
    ]
