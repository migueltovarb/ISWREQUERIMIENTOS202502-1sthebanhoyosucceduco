from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cliente, Pedido, ItemPedido, Producto, CategoriaProducto

class ClienteRegistroForm(UserCreationForm):
    """Formulario para registro de clientes"""
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo'
        })
    )
    telefono = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono'
        })
    )
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña'})


class ClienteLoginForm(AuthenticationForm):
    """Formulario de inicio de sesión"""
    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )


class TipoPedidoForm(forms.Form):
    """Formulario para seleccionar tipo de pedido"""
    TIPO_CHOICES = [
        ('para_llevar', 'Para llevar'),
        ('consumir_lugar', 'Para consumir en el lugar'),
        ('domicilio', 'A domicilio'),
    ]
    
    tipo_pedido = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Seleccione el tipo de pedido'
    )


class DireccionDomicilioForm(forms.Form):
    """Formulario para dirección de domicilio"""
    direccion = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Calle 18 # 22-45, Barrio La Rosa'
        }),
        label='Dirección exacta'
    )
    barrio = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rosa'
        }),
        label='Barrio / Sector'
    )
    telefono = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '31587992562'
        }),
        label='Teléfono de contacto'
    )
    indicaciones = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Torre 3, Apto 502',
            'rows': 3
        }),
        label='Indicaciones adicionales (opcional)'
    )


class CodigoMesaForm(forms.Form):
    """Formulario para código de mesa"""
    codigo_mesa = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'M___',
            'pattern': '[M][0-9]{3}',
        }),
        label='Código de mesa'
    )


class AgregarProductoForm(forms.Form):
    """Formulario para agregar producto al pedido"""
    producto_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control cantidad-input',
            'min': '1'
        })
    )


class ModificarItemForm(forms.Form):
    """Formulario para modificar items del pedido"""
    item_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    accion = forms.ChoiceField(
        choices=[('modificar', 'Modificar'), ('eliminar', 'Eliminar')],
        widget=forms.HiddenInput()
    )


class MetodoPagoForm(forms.Form):
    """Formulario para método de pago"""
    METODO_CHOICES = [
        ('efectivo', 'Efectivo - Paga directamente al momento de recoger o recibir tu pedido'),
        ('tarjeta', 'Tarjeta débito o crédito - Ingresa los datos de tu tarjeta en la pasarela de pago segura'),
        ('digital', 'Pago digital (Nequi / Daviplata) - Escanea el código QR o envía el pago al número 310-555-1234'),
    ]
    
    metodo_pago = forms.ChoiceField(
        choices=METODO_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Selecciona tu método de pago'
    )


class CalificarPedidoForm(forms.Form):
    """Formulario para calificar el pedido"""
    CALIFICACION_CHOICES = [
        (1, '1 estrella - Muy insatisfecho'),
        (2, '2 estrellas - Insatisfecho'),
        (3, '3 estrellas - Neutral'),
        (4, '4 estrellas - Satisfecho'),
        (5, '5 estrellas - Muy satisfecho'),
    ]
    
    calificacion = forms.ChoiceField(
        choices=CALIFICACION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'rating-input'}),
        label='¿Cómo calificarías tu experiencia con este pedido?'
    )
    comentario = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe tu comentario aquí (opcional)',
            'rows': 4
        }),
        label='Comentario (opcional)'
    )


class BuscarProductoForm(forms.Form):
    """Formulario para buscar productos"""
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=CategoriaProducto.objects.all(),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class CancelarPedidoForm(forms.Form):
    """Formulario para confirmar cancelación de pedido"""
    confirmar = forms.BooleanField(
        required=True,
        label='Sí, cancelar pedido',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pedido_id = forms.IntegerField(widget=forms.HiddenInput())