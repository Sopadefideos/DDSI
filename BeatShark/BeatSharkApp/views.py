from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistroUsuario

# Create your views here.

def feed(request):
    return render(request, 'social/feed.html')

def profile(request):
    return render(request, 'social/profile.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
        return redirect('feed')
    else:
        form = RegistroUsuario()
    return render(request, 'social/registro.html', {'form':form})
