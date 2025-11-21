from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator
from decimal import Decimal

class ClienteManager(BaseUserManager):
    def create_user(self, correo, nombre, telefono, password=None):
        if not correo:
            raise ValueError('El cliente debe tener un correo electrónico')
        
        user = self.model(
            correo=self.normalize_email(correo),
            nombre=nombre,
            telefono=telefono
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo, nombre, telefono, password=None):
        user = self.create_user(
            correo=correo,
            nombre=nombre,
            telefono=telefono,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Cliente(AbstractBaseUser, PermissionsMixin):
    IDCliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = ClienteManager()
    
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'telefono']
    
    # Solución al conflicto de relacionados
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='clientes',  # Cambio aquí
        related_query_name='cliente',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='clientes',  # Cambio aquí
        related_query_name='cliente',
    )
    
    def registrarCuenta(self):
        """Método para registrar la cuenta del cliente"""
        self.save()
    
    def iniciarSesion(self):
        """Método simbólico para iniciar sesión"""
        return True
    
    def cancelarPedido(self, pedido):
        """Permite al cliente cancelar un pedido"""
        if pedido.estado in ['pendiente', 'confirmado']:
            pedido.estado = 'cancelado'
            pedido.save()
            return True
        return False
    
    def consultarEstadoPedido(self, pedido):
        """Consulta el estado de un pedido específico"""
        return pedido.estado
    
    def __str__(self):
        return f"{self.nombre} ({self.correo})"

# Empleado ahora es un modelo normal, NO hereda de AbstractBaseUser
class Empleado(models.Model):
    IDEmpleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    usuario = models.CharField(max_length=50, unique=True)
    contraseña = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    
    def registrarUsuario(self):
        """Método para registrar un nuevo usuario empleado"""
        self.save()
    
    def modificarUsuario(self, **kwargs):
        """Modifica los datos del usuario empleado"""
        for field, value in kwargs.items():
            setattr(self, field, value)
        self.save()
    
    def eliminarUsuario(self):
        """Elimina el usuario empleado"""
        self.delete()
    
    def generarReporte(self, tipo_reporte, fecha_inicio, fecha_fin):
        """Genera reportes del sistema"""
        return f"Reporte {tipo_reporte} generado para el período {fecha_inicio} - {fecha_fin}"
    
    def __str__(self):
        return f"Empleado: {self.nombre}"

# Administrador como modelo proxy SIN campos adicionales
class Administrador(Empleado):
    class Meta:
        proxy = True
    
    def __str__(self):
        return f"Administrador: {self.nombre}"

class CategoriaProducto(models.Model):
    IDCategoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    IDProducto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('en_preparacion', 'En Preparación'),
        ('listo', 'Listo para Entregar'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    IDPedido = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(blank=True)
    
    def agregarProducto(self, producto, cantidad=1):
        """Agrega un producto al pedido"""
        item, created = ItemPedido.objects.get_or_create(
            pedido=self,
            producto=producto,
            defaults={'cantidad': cantidad, 'subtotal': producto.precio * cantidad}
        )
        if not created:
            item.cantidad += cantidad
            item.subtotal = item.producto.precio * item.cantidad
            item.save()
        
        self.calcularTotal()
    
    def calcularTotal(self):
        """Calcula el total del pedido sumando todos los items"""
        items = self.items.all()
        self.total = sum(item.subtotal for item in items)
        self.save()
        return self.total
    
    def actualizarEstado(self, nuevo_estado):
        """Actualiza el estado del pedido"""
        if nuevo_estado in dict(self.ESTADOS_PEDIDO):
            self.estado = nuevo_estado
            self.save()
            return True
        return False
    
    def generarComprobante(self):
        """Genera un comprobante del pedido"""
        comprobante = {
            'id_pedido': self.IDPedido,
            'fecha': self.fecha,
            'cliente': self.cliente.nombre,
            'items': [{'producto': item.producto.nombre, 'cantidad': item.cantidad, 'subtotal': item.subtotal} 
                     for item in self.items.all()],
            'total': self.total,
            'estado': self.get_estado_display()
        }
        return comprobante
    
    def __str__(self):
        return f"Pedido #{self.IDPedido} - {self.cliente.nombre} - {self.estado}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        """Calcula el subtotal automáticamente al guardar"""
        self.subtotal = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} - ${self.subtotal}"

class Sistema(models.Model):
    IDSistema = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, default='1.0.0')
    fechaActualizacion = models.DateField(auto_now=True)
    nombre_cafeteria = models.CharField(max_length=100, default='Mi Cafetería')
    
    def __str__(self):
        return f"Sistema v{self.version} - {self.fechaActualizacion}"

class Inventario(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='inventario')
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def necesita_reabastecimiento(self):
        """Verifica si el producto necesita reabastecimiento"""
        return self.stock_actual <= self.stock_minimo
    
    def __str__(self):
        return f"Inventario {self.producto.nombre}: {self.stock_actual} unidades"