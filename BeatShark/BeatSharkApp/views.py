from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .models import *
from passlib.hash import pbkdf2_sha256

# Create your views here.

def index(request):
    # request.session["log"]
    # del request.session["log"]

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

    if(request.GET.get('logout')):
        for key in list(request.session.keys()):
            del request.session[key]
        return HttpResponseRedirect("/")


    return render(request, 'social/index.html')

def register(request):

    if request.POST:

        username = request.POST.get('user')
        password = request.POST.get('password')
        Repassword = request.POST.get('passwordRepeat')
        email = request.POST.get('email')
        if (password == Repassword):
            if (Usuario.objects.filter(nombre=username)):
                messages.info(request, 'El usuario ya existe')
                return HttpResponseRedirect("/%2Fregister")

            if (Usuario.objects.filter(email=email)):
                messages.info(request, 'El email ya existe')
                return HttpResponseRedirect("/%2Fregister")

            enc_password =  pbkdf2_sha256.encrypt(password, rounds=12000, salt_size=32)
            user = Usuario(nombre=username, contraseña=enc_password, email=email)
            user.save()
            return HttpResponseRedirect("/")
        else:
            messages.info(request, 'Las contraseñas no coinciden')
            return HttpResponseRedirect("/%2Fregister")

        

    return render(request, 'social/register.html')