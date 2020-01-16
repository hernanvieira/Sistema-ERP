from django.db import models

from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre',max_length=100, blank=False, null=False)

    def __str__(self):
        return str(self.nombre)


class customuser(AbstractUser):
    rol = models.ForeignKey(Rol,on_delete=models.PROTECT)
