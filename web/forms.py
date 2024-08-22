# forms.py
from django import forms
from .models import Cliente, OrdenDeReparacion, Maquina, Presupuesto, Repuesto
from django.core.exceptions import ValidationError



class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['empresa', 'razon_social', 'nombre', 'apellido', 'condicion_iva', 'email','domicilio', 'localidad', 'codigo_postal', 'telefono','telefono_alternativo',]
        widgets = {
            'empresa': forms.CheckboxInput(attrs={'class': 'form-check-input mt-3', 'style': 'margin: auto; position: relative;'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón Social'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'condicion_iva': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Condición IVA'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'telefono_alternativo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono Alternativo'}),
            
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
        fields = ['garantia', 'categoria', 'subcategoria', 'modelo', 'serie', 'falla', 'accesorios']
        widgets = {
            'garantia': forms.CheckboxInput(),
            'categoria': forms.Select(attrs={'id': 'attrcategoria', 'class': 'form-select'}),
            'subcategoria': forms.Select(attrs={'id': 'attrsubcategoria', 'class': 'form-select'}),
            'modelo': forms.Select(attrs={'id': 'attrmodelo', 'class': 'form-select'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'falla': forms.Select(attrs={'class': 'form-select'}),
            
            
        }

        empty_labels = {
            'categoria': '------',
            'subcategoria': '------',
            'modelo': '------',
            'accesorios':  '------',
        }



class OrdenDeReparacionForm(forms.ModelForm):
    class Meta:
        model = OrdenDeReparacion
        fields = ['cliente', 'notas']
        widgets = {
            'notas': forms.Textarea(attrs={'class': 'form-control', 'style':"height: 435px", 'placeholder': 'Notas'})
        }
        empty_labels = {
            'cliente': '------',
        }


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = [ 'descripcion', 'total']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'style':"height: 435px", 'placeholder': 'Descripcion'})
        }
        
