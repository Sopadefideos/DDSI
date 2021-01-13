from django.db import models
from passlib.hash import pbkdf2_sha256

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    rol = models.SmallIntegerField(default=1)

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.contraseña)

class Genero(models.Model):
    nombre_genero = models.CharField(max_length=50)

class Artista(models.Model):
    nombre = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=20)
    fechaNacimiento = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)

class Album(models.Model):
    nombre = models.CharField(max_length=50)
    num_canciones = models.SmallIntegerField(null=False)
    fechaEstreno = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)

class Cancion(models.Model):
    titulo = models.CharField(max_length=50)
    artista = models.CharField(max_length=50)
    genero = models.OneToOneField(Genero, on_delete=models.CASCADE)

class FavAlbum(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    album = models.OneToOneField(Album, on_delete=models.CASCADE)

class FavCancion(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    cancion = models.OneToOneField(Cancion, on_delete=models.CASCADE)

class FavArtista(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    artista = models.OneToOneField(Artista, on_delete=models.CASCADE)

class AlbumCancion(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    cancion = models.OneToOneField(Cancion, on_delete=models.CASCADE)

class CancionArtista(models.Model):
    cancion = models.OneToOneField(Cancion, on_delete=models.CASCADE)
    artista = models.OneToOneField(Artista, on_delete=models.CASCADE)