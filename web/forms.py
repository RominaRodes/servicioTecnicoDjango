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
        fields = ['categoria', 'subcategoria', 'modelo', 'serie', 'falla', 'garantia', 'accesorios']
        widgets = {
            'categoria': forms.Select(attrs={'id': 'attrcategoria', 'class': 'form-select'}),
            'subcategoria': forms.Select(attrs={'id': 'attrsubcategoria', 'class': 'form-select'}),
            'modelo': forms.Select(attrs={'id': 'attrmodelo', 'class': 'form-select'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'falla': forms.Select(attrs={'class': 'form-select'}),
            'garantia': forms.CheckboxInput(attrs={'class': 'form-check'}),
            'accesorios': forms.CheckboxSelectMultiple(attrs={'id': 'attraccesorios', 'class': 'form-check p-0'}),
        }


class OrdenDeReparacionForm(forms.ModelForm):
    class Meta:
        model = OrdenDeReparacion
        fields = ['cliente', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'notas': forms.Textarea(attrs={'class': 'form-control'})
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = [ 'descripcion', 'total']

        
