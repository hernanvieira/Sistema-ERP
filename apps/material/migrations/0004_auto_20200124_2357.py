# Generated by Django 2.2 on 2020-01-25 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_compra_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]