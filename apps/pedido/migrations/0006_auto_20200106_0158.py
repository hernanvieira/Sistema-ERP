# Generated by Django 2.2 on 2020-01-06 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0005_entregas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregas',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedido.Pedido'),
        ),
    ]