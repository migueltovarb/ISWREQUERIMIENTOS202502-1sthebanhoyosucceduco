from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from decimal import Decimal
from .models import Cliente, Pedido, Producto, CategoriaProducto, ItemPedido
from .forms import (
    ClienteRegistroForm, ClienteLoginForm, TipoPedidoForm,
    DireccionDomicilioForm, CodigoMesaForm, AgregarProductoForm,
    ModificarItemForm, MetodoPagoForm, CalificarPedidoForm,
    BuscarProductoForm, CancelarPedidoForm
)
from django.views.decorators.http import require_POST


# ============ AUTENTICACIÓN ============

def registro_cliente(request):
    """Registro de nuevo cliente"""
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            login(request, cliente)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('inicio_pedido')
    else:
        form = ClienteRegistroForm()
    
    return render(request, 'cafeteria/registro.html', {'form': form})


def login_cliente(request):
    """Inicio de sesión"""
    if request.method == 'POST':
        form = ClienteLoginForm(request, data=request.POST)
        if form.is_valid():
            correo = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=correo, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido, {user.nombre}!')
                return redirect('inicio_pedido')
    else:
        form = ClienteLoginForm()
    
    return render(request, 'cafeteria/login.html', {'form': form})


@login_required
def logout_cliente(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')


# ============ INICIO Y TIPO DE PEDIDO ============

@login_required
def inicio_pedido(request):
    """HU_001: Pantalla de inicio - Comenzar pedido o retomar pedido"""
    # Verificar si hay un pedido activo (en proceso)
    # Buscar el primer pedido que NO esté finalizado (entregado o cancelado)
    pedido_activo = Pedido.objects.filter(cliente=request.user).exclude(estado__in=['entregado', 'cancelado']).first()
    
    context = {
        'pedido_activo': pedido_activo
    }
    return render(request, 'cafeteria/inicio_pedido.html', context)


@login_required
def seleccionar_tipo_pedido(request):
    """HU_006: Seleccionar tipo de pedido"""
    if request.method == 'POST':
        form = TipoPedidoForm(request.POST)
        if form.is_valid():
            tipo = form.cleaned_data['tipo_pedido']
            
            # Crear o recuperar pedido en proceso
            pedido, created = Pedido.objects.get_or_create(
                cliente=request.user,
                estado='pendiente',
                defaults={'total': Decimal('0.00')}
            )
            
            # Guardar tipo en sesión
            request.session['tipo_pedido'] = tipo
            
            # Redirigir según el tipo
            if tipo == 'domicilio':
                return redirect('ingresar_direccion')
            elif tipo == 'consumir_lugar':
                return redirect('ingresar_codigo_mesa')
            else:  # para_llevar
                return redirect('mostrar_menu')
    else:
        form = TipoPedidoForm()
    
    return render(request, 'cafeteria/tipo_pedido.html', {'form': form})


@login_required
def ingresar_direccion(request):
    """HU_007: Introducir dirección para domicilio"""
    if request.method == 'POST':
        form = DireccionDomicilioForm(request.POST)
        if form.is_valid():
            # Guardar dirección en sesión
            request.session['direccion_domicilio'] = {
                'direccion': form.cleaned_data['direccion'],
                'barrio': form.cleaned_data['barrio'],
                'telefono': form.cleaned_data['telefono'],
                'indicaciones': form.cleaned_data['indicaciones']
            }
            messages.success(request, 'Dirección registrada correctamente')
            return redirect('mostrar_menu')
    else:
        form = DireccionDomicilioForm()
    
    return render(request, 'cafeteria/ingresar_direccion.html', {'form': form})


@login_required
def ingresar_codigo_mesa(request):
    """HU_008: Código de mesa"""
    if request.method == 'POST':
        form = CodigoMesaForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo_mesa']
            # Validar formato M + 3 dígitos
            if codigo.startswith('M') and len(codigo) == 4:
                request.session['codigo_mesa'] = codigo
                messages.success(request, f'Mesa {codigo} registrada')
                return redirect('mostrar_menu')
            else:
                messages.error(request, 'Código de mesa inválido')
    else:
        form = CodigoMesaForm()
    
    return render(request, 'cafeteria/codigo_mesa.html', {'form': form})


# ============ MENÚ Y PRODUCTOS ============

@login_required
def mostrar_menu(request):
    """HU_002: Mostrar menú con productos"""
    # Obtener pedido actual
    pedido = Pedido.objects.filter(
        cliente=request.user,
        estado='pendiente'
    ).first()
    
    if not pedido:
        # Crear nuevo pedido si no existe
        pedido = Pedido.objects.create(
            cliente=request.user,
            estado='pendiente',
            total=Decimal('0.00')
        )
    
    # Filtros y búsqueda
    busqueda = request.GET.get('busqueda', '')
    categoria_id = request.GET.get('categoria', '')
    
    productos = Producto.objects.filter(disponible=True)
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    categorias = CategoriaProducto.objects.all()
    form_busqueda = BuscarProductoForm(request.GET)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'pedido': pedido,
        'form_busqueda': form_busqueda
    }
    return render(request, 'cafeteria/menu.html', context)


@login_required
def agregar_producto(request, producto_id):
    """Agregar producto al pedido"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, IDProducto=producto_id, disponible=True)
        pedido = Pedido.objects.filter(
            cliente=request.user,
            estado='pendiente'
        ).first()
        
        if not pedido:
            pedido = Pedido.objects.create(
                cliente=request.user,
                estado='pendiente',
                total=Decimal('0.00')
            )
        
        cantidad = int(request.POST.get('cantidad', 1))
        pedido.agregarProducto(producto, cantidad)
        
        messages.success(request, f'{producto.nombre} agregado al pedido')
        return redirect('mostrar_menu')
    
    return redirect('mostrar_menu')


@login_required
def recomendaciones(request):
    """HU_003: Recomendar productos del menú"""
    pedido = Pedido.objects.filter(
        cliente=request.user,
        estado='pendiente'
    ).first()
    
    # Lógica de recomendaciones basada en:
    # 1. Productos más vendidos
    # 2. Productos similares a los del pedido actual
    # 3. Productos populares
    
    productos_recomendados = Producto.objects.filter(disponible=True).order_by('?')[:6]
    
    context = {
        'productos_recomendados': productos_recomendados,
        'pedido': pedido
    }
    return render(request, 'cafeteria/recomendaciones.html', context)


# ============ GESTIÓN DEL PEDIDO ============

@login_required
def ver_recuento_pedido(request):
    """HU_005: Recuento del pedido antes de confirmar"""
    # Intentar obtener el pedido pendiente; si no existe, crear uno vacío
    pedido = Pedido.objects.filter(
        cliente=request.user,
        estado='pendiente'
    ).first()

    if not pedido:
        pedido = Pedido.objects.create(
            cliente=request.user,
            estado='pendiente',
            total=Decimal('0.00')
        )

    # Asegurar que el total esté actualizado
    pedido.calcularTotal()

    items = pedido.items.all()
    
    context = {
        'pedido': pedido,
        'items': items,
        'tipo_pedido': request.session.get('tipo_pedido', 'para_llevar')
    }
    return render(request, 'cafeteria/recuento_pedido.html', context)


@login_required
def modificar_pedido(request):
    """HU_004: Modificar el pedido"""
    pedido = get_object_or_404(
        Pedido,
        cliente=request.user,
        estado='pendiente'
    )
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        item_id = request.POST.get('item_id')
        
        if accion == 'aumentar':
            item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)
            item.cantidad += 1
            item.save()
            pedido.calcularTotal()
            
        elif accion == 'disminuir':
            item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)
            if item.cantidad > 1:
                item.cantidad -= 1
                item.save()
            else:
                item.delete()
            pedido.calcularTotal()
            
        elif accion == 'eliminar':
            item = get_object_or_404(ItemPedido, id=item_id, pedido=pedido)
            item.delete()
            pedido.calcularTotal()
        
        messages.success(request, 'Pedido actualizado')
        return redirect('modificar_pedido')
    
    items = pedido.items.all()
    context = {
        'pedido': pedido,
        'items': items
    }
    return render(request, 'cafeteria/modificar_pedido.html', context)


@login_required
def seguir_con_pedido(request):
    """Seguir agregando productos al pedido"""
    return redirect('mostrar_menu')


@login_required
def confirmar_pedido(request):
    """Confirmar el pedido y proceder al pago"""
    pedido = get_object_or_404(
        Pedido,
        cliente=request.user,
        estado='pendiente'
    )
    
    if pedido.items.count() == 0:
        messages.error(request, 'No hay productos en el pedido')
        return redirect('mostrar_menu')
    
    return redirect('metodo_pago')


# ============ PAGO ============

@login_required
def metodo_pago(request):
    """HU_010: Métodos de pago"""
    pedido = get_object_or_404(
        Pedido,
        cliente=request.user,
        estado='pendiente'
    )
    
    if request.method == 'POST':
        form = MetodoPagoForm(request.POST)
        if form.is_valid():
            metodo = form.cleaned_data['metodo_pago']
            request.session['metodo_pago'] = metodo
            
            # Aquí se procesaría el pago según el método
            # Por ahora solo confirmamos el pedido
            pedido.estado = 'confirmado'
            pedido.save()
            
            messages.success(request, '¡Pedido confirmado exitosamente!')
            return redirect('factura_pedido', pedido_id=pedido.IDPedido)
    else:
        form = MetodoPagoForm()
    
    context = {
        'form': form,
        'pedido': pedido
    }
    return render(request, 'cafeteria/metodo_pago.html', context)


# ============ FACTURA Y COMPROBANTES ============

@login_required
def factura_pedido(request, pedido_id):
    """HU_011: Factura del pedido"""
    pedido = get_object_or_404(Pedido, IDPedido=pedido_id, cliente=request.user)
    comprobante = pedido.generarComprobante()
    
    context = {
        'pedido': pedido,
        'comprobante': comprobante,
        'items': pedido.items.all(),
        'metodo_pago': request.session.get('metodo_pago', 'Efectivo')
    }
    return render(request, 'cafeteria/factura.html', context)


# ============ SEGUIMIENTO ============

@login_required
def progreso_pedido(request, pedido_id):
    """HU_012: Progreso del pedido"""
    pedido = get_object_or_404(Pedido, IDPedido=pedido_id, cliente=request.user)
    
    # Estados de progreso
    estados_progreso = [
        {'nombre': 'Pedido recibido', 'estado': 'confirmado', 'completado': False},
        {'nombre': 'En preparación', 'estado': 'en_preparacion', 'completado': False},
        {'nombre': 'Listo para entregar', 'estado': 'listo', 'completado': False},
        {'nombre': 'Entregado', 'estado': 'entregado', 'completado': False},
    ]
    
    # Marcar estados completados
    estado_actual_index = -1
    for i, ep in enumerate(estados_progreso):
        if ep['estado'] == pedido.estado:
            estado_actual_index = i
            break
    
    for i in range(estado_actual_index + 1):
        estados_progreso[i]['completado'] = True
    
    context = {
        'pedido': pedido,
        'estados_progreso': estados_progreso,
        'estado_actual': pedido.get_estado_display()
    }
    return render(request, 'cafeteria/progreso_pedido.html', context)


@login_required
@require_POST
def marcar_entregado(request):
    """Marca el pedido pendiente del usuario como 'entregado'. Devuelve JSON con el id del pedido."""
    pedido = Pedido.objects.filter(cliente=request.user, estado__in=['pendiente', 'confirmado', 'en_preparacion', 'listo']).first()
    if not pedido:
        return JsonResponse({'ok': False, 'error': 'No hay pedido en proceso'}, status=400)

    pedido.estado = 'entregado'
    pedido.save()
    # Limpiar datos de sesión asociados al pedido activo
    for k in ['tipo_pedido', 'direccion_domicilio', 'codigo_mesa', 'metodo_pago']:
        try:
            request.session.pop(k, None)
        except Exception:
            pass

    return JsonResponse({'ok': True, 'pedido_id': pedido.IDPedido})


# ============ CALIFICACIÓN ============

@login_required
def calificar_pedido(request, pedido_id):
    """Calificar un pedido completado"""
    pedido = get_object_or_404(
        Pedido,
        IDPedido=pedido_id,
        cliente=request.user,
        estado='entregado'
    )
    
    if request.method == 'POST':
        form = CalificarPedidoForm(request.POST)
        if form.is_valid():
            calificacion = form.cleaned_data['calificacion']
            comentario = form.cleaned_data['comentario']
            
            # Aquí se guardaría la calificación (necesitas un modelo Calificacion)
            # Guardar estado final del pedido y persistir (asegurar que no quede como activo)
            if pedido.estado != 'entregado':
                pedido.estado = 'entregado'
                pedido.save()
            # Limpiar sesión para que no quede como pedido activo
            for k in ['tipo_pedido', 'direccion_domicilio', 'codigo_mesa', 'metodo_pago']:
                try:
                    request.session.pop(k, None)
                except Exception:
                    pass

            # Aquí se podría crear y guardar un objeto Calificacion si existiera
            messages.success(request, '¡Gracias por tu calificación! Pedido enviado al historial.')
            return redirect('historial')
    else:
        form = CalificarPedidoForm()
    
    context = {
        'form': form,
        'pedido': pedido
    }
    return render(request, 'cafeteria/calificar_pedido.html', context)


# ============ CANCELACIÓN ============

@login_required
def cancelar_pedido(request, pedido_id):
    """HU_009: Cancelar el pedido"""
    pedido = get_object_or_404(
        Pedido,
        IDPedido=pedido_id,
        cliente=request.user
    )
    
    # Solo se puede cancelar si está en ciertos estados
    if pedido.estado not in ['pendiente', 'confirmado']:
        messages.error(request, 'Este pedido no puede ser cancelado')
        return redirect('progreso_pedido', pedido_id=pedido_id)
    
    if request.method == 'POST':
        form = CancelarPedidoForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmar']:
            pedido.estado = 'cancelado'
            pedido.save()
            messages.success(request, 'Pedido cancelado exitosamente')
            return redirect('inicio_pedido')
    else:
        form = CancelarPedidoForm(initial={'pedido_id': pedido_id})
    
    context = {
        'form': form,
        'pedido': pedido
    }
    return render(request, 'cafeteria/cancelar_pedido.html', context)


# ============ HISTORIAL ============

@login_required
def historial_pedidos(request):
    """Ver historial de pedidos del cliente"""
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-fecha')
    
    context = {
        'pedidos': pedidos
    }
    return render(request, 'cafeteria/historial.html', context)