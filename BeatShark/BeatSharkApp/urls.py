from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('edit/', views.admin, name='edit'),
    path('fav/', views.fav, name='fav'),
    path('edit/mod/', views.mod, name='mod'),
    path('edit/add/', views.add, name='add')
]
