# forms.py
from django import forms
from .models import Cliente, OrdenDeReparacion, Maquina, Presupuesto, Repuesto
from django.core.exceptions import ValidationError

from django import forms
from .models import Cliente
from django.core.exceptions import ValidationError
import re

class ClienteForm(forms.ModelForm): 
    class Meta:
        model = Cliente
        fields = [
            'nombre', 'empresa', 'razon_social', 'contacto', 'condicion_iva', 
            'cuit', 'dni', 'tipo_cliente', 'domicilio', 'localidad', 'provincia', 
            'codigo_postal', 'telefono', 'telefono_alternativo', 'email'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'empresa': forms.CheckboxInput(attrs={'class': 'form-check-input mt-3', 'style': 'margin: auto; position: relative;'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón Social'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre y apellido del contacto'}),
            'condicion_iva': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Condición IVA'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CUIT'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            'provincia': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Provincia'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'telefono_alternativo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono Alternativo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    def clean_cuit(self):
        cuit = self.cleaned_data.get('cuit')  # Obtiene el valor del CUIT
        if cuit:  # Solo aplica el replace si cuit no es None o no está vacío
            cuit = cuit.replace('-', '')
            if not re.match(r'^\d{11}$', cuit):
                raise ValidationError('El CUIT debe tener 11 dígitos numéricos.')
        return cuit  # Si el CUIT está vacío, permite que continúe vacío

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni and (len(dni) != 8 or not dni.isdigit()):
            raise ValidationError('El DNI debe tener exactamente 8 dígitos.')
        return dni

    def clean_contacto(self):
        contacto = self.cleaned_data.get('contacto')
        if contacto and not contacto.replace(' ', '').isalpha():
            raise ValidationError("El nombre del contacto solo debe contener letras.")
        return contacto

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')
        cuit = cleaned_data.get('cuit')
        dni = cleaned_data.get('dni')
        razon_social = cleaned_data.get('razon_social')

        if empresa:
            if not razon_social:
                self.add_error('razon_social', 'Razón Social es obligatoria para empresas.')
            if not cuit:
                self.add_error('cuit', 'CUIT es obligatorio para empresas.')
        else:
            if not dni:
                self.add_error('dni', 'DNI es obligatorio para particulares.')
            if razon_social:
                self.add_error('razon_social', 'Razón Social no debe completarse para particulares.')

        return cleaned_data

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
        
