# forms.py
from django import forms
from .models import Cliente, OrdenDeReparacion, Maquina, Presupuesto, Repuesto
from django.core.exceptions import ValidationError




class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'empresa', 'razon_social', 'condicion_iva', 'domicilio', 'localidad', 'codigo_postal', 'telefono', 'email']
        widgets = {
            'empresa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DetalleClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True

class MaquinaForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = '__all__'
        widgets = {
            'categoria': forms.Select(attrs={'id': 'attrcategoria'}),
            'subcategoria': forms.Select(attrs={'id': 'attrsubcategoria'}),
            'modelo': forms.Select(attrs={'id': 'attrmodelo'}),
            'accesorios': forms.CheckboxSelectMultiple(attrs={'id': 'attraccesorios'}),  # Este ya es un CheckboxSelectMultiple
        }

class OrdenDeReparacionForm(forms.ModelForm):
    class Meta:
        model = OrdenDeReparacion
        fields = ['cliente', 'notas']

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = [ 'descripcion', 'total']

        
