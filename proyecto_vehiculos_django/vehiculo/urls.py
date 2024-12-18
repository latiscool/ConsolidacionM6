from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexView, name="index"),
    path("vehiculo/add/", views.agregar_vehiculoView, name="agregar_vehiculo"),
    path("vehiculos/", views.listar_vehiculosView, name="listar_vehiculos"),
    path("register/", views.register, name="register"),
]
