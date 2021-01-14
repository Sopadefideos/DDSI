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

    canciones = Cancion.objects.all()

    print(canciones[0].artista.all()[0].nombre)
    

    return render(request, 'social/index.html', {'canciones': canciones})

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

    ########## DELETE ########
    if (request.POST.get('delete')):
        userId = request.POST.get('delete')
        Usuario.objects.filter(id=userId).delete()
        return HttpResponseRedirect("/edit")

    ########## CHANGE ROL ########
    if (request.POST.get('rol')):
        newRol = request.POST.get('rol')
        userId = request.POST.get('userId')

        userUpdate = Usuario.objects.get(id=userId)
        userUpdate.rol = newRol

        userUpdate.save(force_update=True)
        return HttpResponseRedirect("/edit")
    
    usuarios = Usuario.objects.all()
    return render(request, 'social/admin.html', {'usuarios': usuarios})


