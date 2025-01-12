# forms.py
from django import forms
from .models import Cliente, OrdenDeReparacion, Maquina, Presupuesto, Repuesto, RepuestoPresupuesto
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
import re
import decimal



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
        fields = ['garantia', 'categoria', 'subcategoria', 'modelo', 'serie', 'accesorios']
        widgets = {
            'garantia': forms.CheckboxInput(),
            'categoria': forms.Select(attrs={'id': 'attrcategoria', 'class': 'form-select'}),
            'subcategoria': forms.Select(attrs={'id': 'attrsubcategoria', 'class': 'form-select'}),
            'modelo': forms.Select(attrs={'id': 'attrmodelo', 'class': 'form-select'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}), 
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
            'notas': forms.Textarea(attrs={'class': 'form-control', 'style':"height: 350px", 'placeholder': 'Notas'})
        }
        empty_labels = {
            'cliente': '------',
        }



class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['descripcion', 'nota_interna', 'total_estimado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción',  'style':"height: 250px"}),
            'nota_interna': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Nota Interna',  'style':"height: 250px"}),
            'total_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Estimado'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if not descripcion:
            raise forms.ValidationError("La descripción es obligatoria.")
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        return descripcion

    def clean_total_estimado(self):
        total_estimado = self.cleaned_data.get('total_estimado')
        if total_estimado is None:
            raise forms.ValidationError("El total estimado es obligatorio.")
        try:
            total_estimado = decimal.Decimal(total_estimado)
        except decimal.InvalidOperation:
            raise forms.ValidationError("El total estimado debe ser un número decimal válido.")
        if total_estimado <= 0:
            raise forms.ValidationError("El total estimado debe ser mayor a 0.")
        return total_estimado

    def clean(self):
        cleaned_data = super().clean()
        repuestos_ids = self.data.getlist('repuesto_id')
        cantidades = self.data.getlist('cantidad')

        if repuestos_ids and cantidades:
            for idx, repuesto_id in enumerate(repuestos_ids):
                if not repuesto_id:
                    raise forms.ValidationError(f"El repuesto en la fila {idx + 1} no es válido.")
                
                try:
                    repuesto = Repuesto.objects.get(id=repuesto_id)
                except Repuesto.DoesNotExist:
                    raise forms.ValidationError(f"El repuesto con ID {repuesto_id} no existe.")
                
                try:
                    cantidad = int(cantidades[idx])
                    if cantidad <= 0:
                        raise forms.ValidationError(f"La cantidad para el repuesto {repuesto.nombre} debe ser mayor a 0.")
                    if cantidad > repuesto.stock:
                        raise forms.ValidationError(f"La cantidad para el repuesto {repuesto.nombre} ({cantidad}) excede el stock disponible ({repuesto.stock}).")
                except ValueError:
                    raise forms.ValidationError(f"La cantidad en la fila {idx + 1} debe ser un número entero válido.")

        return cleaned_data




class CrearRepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['nombre', 'categoria', 'codigo', 'precio', 'costo_ultima_compra',  'stock','stock_critico', 'ubicacion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en USD'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad Inicial'}),
            'costo_ultima_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo Unitario Inicial'}),
            'stock_critico': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Crítico'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre:
            raise forms.ValidationError("El campo 'Nombre' es obligatorio.")
        if Repuesto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError("El nombre ya está registrado.")
        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if not codigo:
            raise forms.ValidationError("El campo 'Código' es obligatorio.")
        if Repuesto.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("El código ya está registrado.")
        return codigo

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if not precio or precio <= 0:
            raise forms.ValidationError("El campo 'Precio' es obligatorio y debe ser un número positivo.")
        return precio

    def clean_costo_ultima_compra(self):
        costo_ultima_compra = self.cleaned_data.get('costo_ultima_compra')

        if costo_ultima_compra is not None:
            if costo_ultima_compra <= 0:
                raise forms.ValidationError("El costo unitario debe ser un número positivo.")
        return costo_ultima_compra
    def clean_stock(self):
            stock = self.cleaned_data.get('stock')
            if stock is None or stock < 0:
                raise forms.ValidationError("El campo 'Cantidad Inicial' es obligatorio y debe ser 0 o un número positivo.")
            return stock
    

    def clean_stock_critico(self):
        stock_critico = self.cleaned_data.get('stock_critico')
        if stock_critico is None or stock_critico < 0:
            raise forms.ValidationError("El campo 'Stock Crítico' es obligatorio y debe ser 0 o un número positivo.")
        return stock_critico

    def clean_ubicacion(self):
        ubicacion = self.cleaned_data.get('ubicacion')
        if not ubicacion:
            raise forms.ValidationError("El campo 'Ubicación' es obligatorio.")
        return ubicacion
    
    

class EditarRepuestoForm(forms.ModelForm):
    class Meta:
        model = Repuesto
        fields = ['nombre', 'categoria', 'codigo', 'precio', 'stock_critico', 'ubicacion']  # Sin 'cantidad_actual'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio en USD'}),
            'stock_critico': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Crítico'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ubicación'}),
        }
