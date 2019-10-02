# Generated by Django 2.2 on 2019-10-02 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('material', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id_componente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Componente',
                'verbose_name_plural': 'Componentes',
                'ordering': ['id_componente'],
            },
        ),
        migrations.CreateModel(
            name='Tipo_prenda',
            fields=[
                ('id_tipo_prenda', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('componente', models.ManyToManyField(to='prenda.Componente')),
            ],
            options={
                'verbose_name': 'Tipo de Prenda',
                'verbose_name_plural': 'Tipos de Prenda',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Prenda',
            fields=[
                ('id_prenda', models.AutoField(primary_key=True, serialize=False)),
                ('talle', models.IntegerField()),
                ('tiempo_prod_prenda', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_prenda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='prenda.Tipo_prenda')),
            ],
            options={
                'verbose_name': 'Prenda',
                'verbose_name_plural': 'Prenda',
                'ordering': ['id_prenda'],
            },
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id_ingrediente', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('componente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='prenda.Componente')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='material.Material')),
                ('prenda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='prenda.Prenda')),
            ],
            options={
                'verbose_name': 'Ingrediente',
                'verbose_name_plural': 'Ingrediente',
                'ordering': ['id_ingrediente'],
            },
        ),
    ]
