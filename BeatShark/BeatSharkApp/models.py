from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    contraseña = models.CharField(max_length=20)
    email = models.EmailField()
    rol = models.SmallIntegerField(default=1)

class Genero(models.Model):
    tipo = models.CharField(max_length=50)

class Cancion(models.Model):
    titulo = models.CharField(max_length=50)
    artista = models.CharField(max_length=50)
    genero = models.OneToOneField(Genero, on_delete=models.CASCADE)
