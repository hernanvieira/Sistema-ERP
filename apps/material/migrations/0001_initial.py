# Generated by Django 2.2 on 2019-09-30 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Unidad_medida',
            fields=[
                ('id_unidad', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Unidad_medida',
                'verbose_name_plural': 'Unidad_medida',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tipo_material',
            fields=[
                ('id_tipo_material', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('unidad_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.Unidad_medida')),
            ],
            options={
                'verbose_name': 'Tipo de Material',
                'verbose_name_plural': 'Tipos de materiales',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id_material', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('stock', models.PositiveIntegerField()),
                ('tipo_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='material.Tipo_material')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materiales',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('cantidad', models.PositiveIntegerField()),
                ('material', models.ManyToManyField(to='material.Material')),
            ],
        ),
    ]
