from django.shortcuts import render, redirect
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm


# Vista para la página principal
def indexView(request):
    return render(request, "index.html")


# Vista para agregar vehículos
@login_required
@permission_required("vehiculo.add_vehiculo", raise_exception=True)
def agregar_vehiculoView(request):
    if request.method == "POST":
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = VehiculoForm()
    return render(request, "agregar_vehiculo.html", {"form": form})


# Vista para listar vehículos
@login_required
@permission_required("vehiculo.visualizar_catalogo", raise_exception=True)
def listar_vehiculosView(request):
    vehiculos = Vehiculo.objects.all()
    for vehiculo in vehiculos:
        if vehiculo.precio <= 10000:
            vehiculo.condicion = "Bajo"
        elif 10000 < vehiculo.precio <= 30000:
            vehiculo.condicion = "Medio"
        else:
            vehiculo.condicion = "Alto"
    return render(request, "listar_vehiculos.html", {"vehiculos": vehiculos})


# Vista para el registro de usuarios
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Vehiculo


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        try:
            if form.is_valid():
                # Guardar el usuario
                user = form.save()

                # Asignar permiso visualizar_catalogo al nuevo usuario
                content_type = ContentType.objects.get_for_model(Vehiculo)
                permission = Permission.objects.get(
                    codename="visualizar_catalogo",
                    content_type=content_type,
                )
                user.user_permissions.add(permission)

                # Mensaje de éxito
                messages.success(
                    request,
                    "Usuario registrado exitosamente. Por favor, inicie sesión.",
                )
                return redirect("login")
            else:
                # Mensaje de error si el formulario no es válido
                messages.error(
                    request, "Error en el formulario. Por favor, verifique los datos."
                )
        except Exception as e:
            # Mensaje de error si ocurre una excepción
            messages.error(request, f"Error al registrar usuario: {str(e)}")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})
