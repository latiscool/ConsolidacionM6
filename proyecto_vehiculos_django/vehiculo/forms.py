from django import forms
from .models import Vehiculo


# Formulario para ingresar vehículos
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            "marca",
            "modelo",
            "serial_carroceria",
            "serial_motor",
            "categoria",
            "precio",
        ]
