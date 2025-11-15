from django import forms
from django.forms import widgets
from .models import vehiculo

# creating a form

class vehiculoForm(forms.ModelForm):
    class Meta:
        # write the name of models for which the form is made
        model = vehiculo
        # write the fields of the model for which the form is to be made
        fields = ['placa', 'marca', 'modelo', 'color']

        labels = {
            'placa': 'Número de placa',
            'marca': 'Marca del vehículo',
            'modelo': 'Modelo del vehículo',
            'color': 'Color del vehículo',
        }

        widgets = {
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.Select(attrs={'class': 'form-select'}),
        }
