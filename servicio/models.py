from django.db import models
from django.contrib.auth.models import User

class Opciones(models.Model):
    id = models.AutoField(primary_key=True)
    opciones = models.CharField(max_length=255)

    def __str__(self):
        return self.opciones

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class CasinoColacion(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_servicio = models.DateField()
    id_opciones = models.ForeignKey(Opciones, on_delete=models.CASCADE)
    id_estado = models.IntegerField(choices=[(0, 'No visible'), (1, 'visible')], default=1)
    fecha_actualizacion = models.DateTimeField(auto_now_add=True)  # Agrega la fecha de creación

    def __str__(self):
        return self.titulo
    


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=255)

    def __str__(self):
        return self.tipo

class Usuarios(models.Model):
    rut = models.CharField(max_length=12)  # rut tiene 12 caracteres
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    activo = models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Programacion(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    casino_colacion = models.ForeignKey(CasinoColacion, on_delete=models.CASCADE)
    fecha_servicio = models.DateField()
    cantidad_almuerzo = models.IntegerField(default=1)  # Por defecto 1 para usuario simple, +1 para superusuario
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    impreso = models.IntegerField(choices=[(0, 'No Impreso'), (1, 'Impreso')], default=0)

    def __str__(self):
        return f"Programación para {self.usuario} en {self.casino_colacion} el {self.fecha_servicio}"
    
    
