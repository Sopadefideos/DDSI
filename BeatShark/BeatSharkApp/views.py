from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from passlib.hash import pbkdf2_sha256

#VISTAS!!

def index(request):
    
    ########## LOGIN ########
    if(request.POST.get('user')):
        user = request.POST.get('user')
        password = request.POST.get('password')

        if (Usuario.objects.filter(nombre=user)):
            if (Usuario.verify_password(Usuario.objects.get(nombre=user), password)):
                request.session["user"] = user
                UserRol = Usuario.objects.get(nombre=user)
                request.session["rol"] = UserRol.rol
                return HttpResponseRedirect("/")
            else:
                messages.info(request, 'La contraseña no coincide')
                return HttpResponseRedirect("/")
        else:
            messages.info(request, 'El usuario no existe')
            return HttpResponseRedirect("/")
    
    ########## LOGOUT ########
    if(request.GET.get('logout')):
        for key in list(request.session.keys()):
            del request.session[key]
        return HttpResponseRedirect("/")
    
    ########## ADD FAV SONG ########
    if(request.POST.get('favIdCancion')):
        id_cancion = request.POST.get('favIdCancion')
        id_usuario = request.session["user"]

        user = Usuario.objects.get(nombre=id_usuario)
        song = Cancion.objects.get(id=id_cancion)

        try:
            FavCancion.objects.get(usuario=user, cancion=song)
            messages.info(request, 'Ya esta añadida a Favoritos')
            return HttpResponseRedirect("/")
        except:
            new_fav = FavCancion.objects.create()
            new_fav.cancion.add(song)
            new_fav.usuario.add(user)
            
            new_fav.save()
            return HttpResponseRedirect("/")

    ########## ADD FAV ARTISTA ########
    if(request.POST.get('favIdArtista')):
        id_artista = request.POST.get('favIdArtista')
        id_usuario = request.session["user"]

        user = Usuario.objects.get(nombre=id_usuario)
        artista = Artista.objects.get(id=id_artista)

        try:
            FavArtista.objects.get(usuario=user, artista=artista)
            messages.info(request, 'Ya esta añadida a Favoritos')
            return HttpResponseRedirect("/")
        except:
            new_fav = FavArtista.objects.create()
            new_fav.artista.add(artista)
            new_fav.usuario.add(user)
            
            new_fav.save()
            return HttpResponseRedirect("/")

    ########## ADD FAV ALBUM ########
    if(request.POST.get('favIdAlbum')):
        id_album = request.POST.get('favIdAlbum')
        id_usuario = request.session["user"]

        user = Usuario.objects.get(nombre=id_usuario)
        album = Album.objects.get(id=id_album)

        try:
            FavAlbum.objects.get(usuario=user, album=album)
            messages.info(request, 'Ya esta añadida a Favoritos')
            return HttpResponseRedirect("/")
        except:
            new_fav = FavAlbum.objects.create()
            new_fav.album.add(album)
            new_fav.usuario.add(user)
            
            new_fav.save()
            return HttpResponseRedirect("/")
    
     ########## SEARCH ########
    if (request.GET.get('search')):
        busca = request.GET.get('search')
        canciones = Cancion.objects.filter(titulo=busca)
        artistas = Artista.objects.filter(nombre=busca)
        albumes = Album.objects.filter(nombre=busca)
        return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas,
        'albumes': albumes})


    canciones = Cancion.objects.all()
    artistas = Artista.objects.all()
    albumes = Album.objects.all()

    return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas, 'albumes': albumes})

def register(request):

    ########## REGISTER ########
    if request.POST:

        username = request.POST.get('user')
        password = request.POST.get('password')
        Repassword = request.POST.get('passwordRepeat')
        email = request.POST.get('email')
        if (password == Repassword):
            if (Usuario.objects.filter(nombre=username)):
                messages.info(request, 'El usuario ya existe')
                return HttpResponseRedirect("/register")

            if (Usuario.objects.filter(email=email)):
                messages.info(request, 'El email ya existe')
                return HttpResponseRedirect("/register")

            enc_password =  pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            user = Usuario(nombre=username, contraseña=enc_password, email=email)
            user.save()
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Las contraseñas no coinciden')
            return HttpResponseRedirect("/register")

    return render(request, 'social/register.html')


def admin(request):
    ########## LOGOUT ########
    if(request.GET.get('logout')):
        for key in list(request.session.keys()):
            del request.session[key]
        return HttpResponseRedirect("/")

    ########## LOGIN ########
    if(request.POST.get('user')):
        user = request.POST.get('user')
        password = request.POST.get('password')

        if (Usuario.objects.filter(nombre=user)):
            if (Usuario.verify_password(Usuario.objects.get(nombre=user), password)):
                request.session["user"] = user
                UserRol = Usuario.objects.get(nombre=user)
                request.session["rol"] = UserRol.rol
                return HttpResponseRedirect("/")
            else:
                messages.info(request, 'La contraseña no coincide')
                return HttpResponseRedirect("/")
        else:
            messages.info(request, 'El usuario no existe')
            return HttpResponseRedirect("/")

    ########## DELETE USER ########
    if (request.POST.get('deleteUser')):
        userId = request.POST.get('deleteUser')
        Usuario.objects.filter(id=userId).delete()
        return HttpResponseRedirect("/edit")

    ########## DELETE GENERO ########
    if (request.POST.get('deleteGenero')):
        generoId = request.POST.get('deleteGenero')
        Genero.objects.filter(id=generoId).delete()
        return HttpResponseRedirect("/edit")

    ########## DELETE ARTIST ########
    if (request.POST.get('deleteArtist')):
        artistId = request.POST.get('deleteArtist')
        artista = Artista.objects.get(id=artistId)
        Cancion.objects.filter(artista=artista).delete()
        Artista.objects.filter(id=artistId).delete()
        return HttpResponseRedirect("/edit")

     ########## DELETE CANCION ########
    if (request.POST.get('deleteCancion')):
        canciontId = request.POST.get('deleteCancion')
        Cancion.objects.filter(id=canciontId).delete()
        return HttpResponseRedirect("/edit")

    ########## DELETE ALBUM ########
    if (request.POST.get('deleteAlbum')):
        albumtId = request.POST.get('deleteAlbum')
        Album.objects.filter(id=albumtId).delete()
        return HttpResponseRedirect("/edit")

    ########## CHANGE ROL ########
    if (request.POST.get('rol')):
        newRol = request.POST.get('rol')
        userId = request.POST.get('userId')

        userUpdate = Usuario.objects.get(id=userId)
        userUpdate.rol = newRol

        userUpdate.save(force_update=True)
        return HttpResponseRedirect("/edit")

     ########## SEARCH ########
    if (request.GET.get('search')):
        busca = request.GET.get('search')
        canciones = Cancion.objects.filter(titulo=busca)
        artistas = Artista.objects.filter(nombre=busca)
        albumes = Album.objects.filter(nombre=busca)
        return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas,
        'albumes': albumes})
    
    canciones = Cancion.objects.all()
    usuarios = Usuario.objects.all()
    artistas = Artista.objects.all()
    albumes = Album.objects.all()
    generos = Genero.objects.all()
    return render(request, 'social/admin.html', {'canciones': canciones, 'artistas': artistas,
     'albumes': albumes, 'usuarios': usuarios, 'generos': generos})


def fav(request):
    ########## LOGOUT ########
    if(request.GET.get('logout')):
        for key in list(request.session.keys()):
            del request.session[key]
        return HttpResponseRedirect("/")

    ########## LOGIN ########
    if(request.POST.get('user')):
        user = request.POST.get('user')
        password = request.POST.get('password')

        if (Usuario.objects.filter(nombre=user)):
            if (Usuario.verify_password(Usuario.objects.get(nombre=user), password)):
                request.session["user"] = user
                UserRol = Usuario.objects.get(nombre=user)
                request.session["rol"] = UserRol.rol
                return HttpResponseRedirect("/")
            else:
                messages.info(request, 'La contraseña no coincide')
                return HttpResponseRedirect("/")
        else:
            messages.info(request, 'El usuario no existe')
            return HttpResponseRedirect("/")
    
    ########## DELETE FAV CANCION ########
    if (request.POST.get('deleteCancion')):
        favIdCancion = request.POST.get('deleteCancion')
        nombre_user = request.session["user"]
        FavCancion.objects.get(id=favIdCancion).delete()
        return HttpResponseRedirect("/fav/?userid=" + nombre_user)

    ########## DELETE FAV CANCION ########
    if (request.POST.get('deleteAlbum')):
        favIdAlbum = request.POST.get('deleteAlbum')
        nombre_user = request.session["user"]
        FavAlbum.objects.get(id=favIdAlbum).delete()
        return HttpResponseRedirect("/fav/?userid=" + nombre_user)

    ########## DELETE FAV CANCION ########
    if (request.POST.get('deleteArtista')):
        favIdArtista = request.POST.get('deleteArtista')
        nombre_user = request.session["user"]
        FavArtista.objects.get(id=favIdArtista).delete()
        return HttpResponseRedirect("/fav/?userid=" + nombre_user)
    
    ########## PASSING LIST OF FAV ########
    if (request.session.get('user')):
        nombre_user = request.session["user"]
        usuario = Usuario.objects.get(nombre=nombre_user)
        lista_favCancion = FavCancion.objects.filter(usuario=usuario)
        lista_favAlbum = FavAlbum.objects.filter(usuario=usuario)
        lista_favArtista = FavArtista.objects.filter(usuario=usuario)
        return render(request, 'social/fav.html', {'lista_favCancion': lista_favCancion, 'lista_favAlbum': lista_favAlbum, 'lista_favArtista': lista_favArtista})

     ########## SEARCH ########
    if (request.GET.get('search')):
        busca = request.GET.get('search')
        canciones = Cancion.objects.filter(titulo=busca)
        artistas = Artista.objects.filter(nombre=busca)
        albumes = Album.objects.filter(nombre=busca)
        return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas,
        'albumes': albumes})
        
    return render(request, 'social/fav.html')

def mod(request):

    ########## MOD ARTISTA ########
    if (request.GET.get('idArtista')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newCity = request.POST.get('nacionalidad')
            newDate = request.POST.get('fechaNacimiento')
            newArtist = Artista(id=request.GET.get('idArtista'), nombre=newName, nacionalidad=newCity, fechaNacimiento=newDate)
            newArtist.save(force_update=True)
            return HttpResponseRedirect("/edit")

    ########## MOD GENERO ########
    if (request.GET.get('idGenero')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newGenero = Genero(id=request.GET.get('idGenero'), nombre_genero=newName)
            newGenero.save(force_update=True)
            return HttpResponseRedirect("/edit")

    ########## MOD CANCION ########
    if (request.GET.get('idCancion')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newArtist = request.POST.get('artista')
            newGenero = request.POST.get('genero')
            artist = Artista.objects.get(nombre=newArtist)
            gen = Genero.objects.get(nombre_genero=newGenero)
            newCancion = Cancion(id=request.GET.get('idCancion'), titulo=newName)
            newCancion.save(force_update=True)
            newCancion.artista.add(artist)
            newCancion.genero.add(gen)
            return HttpResponseRedirect("/edit")
            
    ########## MOD GENERO ########
    if (request.GET.get('idAlbum')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newNumCanciones = request.POST.get('numCanciones')
            newDate = request.POST.get('fechaEstreno')
            newAlbum = Album(id=request.GET.get('idAlbum'), nombre=newName, num_canciones=newNumCanciones, fechaEstreno=newDate)
            newAlbum.save(force_update=True)
            return HttpResponseRedirect("/edit")

     ########## SEARCH ########
    if (request.GET.get('search')):
        busca = request.GET.get('search')
        canciones = Cancion.objects.filter(titulo=busca)
        artistas = Artista.objects.filter(nombre=busca)
        albumes = Album.objects.filter(nombre=busca)
        return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas,
        'albumes': albumes})


    canciones = Cancion.objects.all()
    usuarios = Usuario.objects.all()
    artistas = Artista.objects.all()
    albumes = Album.objects.all()
    generos = Genero.objects.all()
    return render(request, 'social/mod.html', {'canciones': canciones, 'artistas': artistas,
     'albumes': albumes, 'usuarios': usuarios, 'generos': generos})


def add(request):

    ########## ARTISTA ########
    if (request.GET.get('Artista')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newCity = request.POST.get('nacionalidad')
            newDate = request.POST.get('fechaNacimiento')
            newArtist = Artista(nombre=newName, nacionalidad=newCity, fechaNacimiento=newDate)
            newArtist.save()
            return HttpResponseRedirect("/edit")

    ########## GENERO ########
    if (request.GET.get('Genero')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newGenero = Genero(nombre_genero=newName)
            newGenero.save()
            return HttpResponseRedirect("/edit")

    ########## CANCION ########
    if (request.GET.get('Cancion')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newArtist = request.POST.get('artista')
            newGenero = request.POST.get('genero')
            artist = Artista.objects.get(nombre=newArtist)
            gen = Genero.objects.get(nombre_genero=newGenero)
            newCancion = Cancion(titulo=newName)
            newCancion.save()
            newCancion.artista.add(artist)
            newCancion.genero.add(gen)
            return HttpResponseRedirect("/edit")
            
    ########## GENERO ########
    if (request.GET.get('Album')):
        if(request.POST.get('nombre')):
            newName = request.POST.get('nombre')
            newNumCanciones = request.POST.get('numCanciones')
            newDate = request.POST.get('fechaEstreno')
            newAlbum = Album(nombre=newName, num_canciones=newNumCanciones, fechaEstreno=newDate)
            newAlbum.save()
            return HttpResponseRedirect("/edit")

    ########## USUARIO ########
    if (request.GET.get('Usuario')):
        if(request.POST.get('user')):
            username = request.POST.get('user')
            password = request.POST.get('password')
            Repassword = request.POST.get('passwordRepeat')
            email = request.POST.get('email')
            if (password == Repassword):
                if (Usuario.objects.filter(nombre=username)):
                    messages.info(request, 'El usuario ya existe')
                    return HttpResponseRedirect("/edit/add/?Usuario=yes")

                if (Usuario.objects.filter(email=email)):
                    messages.info(request, 'El email ya existe')
                    return HttpResponseRedirect("/edit/add/?Usuario=yes")

                enc_password =  pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
                user = Usuario(nombre=username, contraseña=enc_password, email=email)
                user.save()
                return HttpResponseRedirect("/edit")
            else:
                messages.info(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect("/edit/add/?Usuario=yes")

    ########## SEARCH ########
    if (request.GET.get('search')):
        busca = request.GET.get('search')
        canciones = Cancion.objects.filter(titulo=busca)
        artistas = Artista.objects.filter(nombre=busca)
        albumes = Album.objects.filter(nombre=busca)
        return render(request, 'social/index.html', {'canciones': canciones, 'artistas': artistas,
        'albumes': albumes})


    canciones = Cancion.objects.all()
    usuarios = Usuario.objects.all()
    artistas = Artista.objects.all()
    albumes = Album.objects.all()
    generos = Genero.objects.all()
    return render(request, 'social/add.html', {'canciones': canciones, 'artistas': artistas,
     'albumes': albumes, 'usuarios': usuarios, 'generos': generos})