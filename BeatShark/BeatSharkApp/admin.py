from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Genero)
admin.site.register(Artista)
admin.site.register(Album)
admin.site.register(Cancion)
admin.site.register(FavAlbum)
admin.site.register(FavCancion)
admin.site.register(FavArtista)
admin.site.register(AlbumCancion)
admin.site.register(CancionArtista)