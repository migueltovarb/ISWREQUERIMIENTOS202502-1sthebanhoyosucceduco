from django.urls import path
from . import views

urlpatterns = [
    # ============ AUTENTICACIÓN ============
    path('registro/', views.registro_cliente, name='registro'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_cliente, name='logout'),
    
    # ============ INICIO Y TIPO DE PEDIDO ============
    path('', views.inicio_pedido, name='inicio_pedido'),
    path('tipo-pedido/', views.seleccionar_tipo_pedido, name='tipo_pedido'),
    path('direccion/', views.ingresar_direccion, name='ingresar_direccion'),
    path('codigo-mesa/', views.ingresar_codigo_mesa, name='ingresar_codigo_mesa'),
    
    # ============ MENÚ Y PRODUCTOS ============
    path('menu/', views.mostrar_menu, name='mostrar_menu'),
    path('agregar-producto/<int:producto_id>/', views.agregar_producto, name='agregar_producto'),
    path('recomendaciones/', views.recomendaciones, name='recomendaciones'),
    
    # ============ GESTIÓN DEL PEDIDO ============
    path('recuento/', views.ver_recuento_pedido, name='recuento_pedido'),
    path('modificar-pedido/', views.modificar_pedido, name='modificar_pedido'),
    path('seguir-pedido/', views.seguir_con_pedido, name='seguir_pedido'),
    path('confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    
    # ============ PAGO ============
    path('metodo-pago/', views.metodo_pago, name='metodo_pago'),
    path('marcar-entregado/', views.marcar_entregado, name='marcar_entregado'),
    
    # ============ FACTURA Y SEGUIMIENTO ============
    path('factura/<int:pedido_id>/', views.factura_pedido, name='factura_pedido'),
    path('progreso/<int:pedido_id>/', views.progreso_pedido, name='progreso_pedido'),
    
    # ============ CALIFICACIÓN ============
    path('calificar/<int:pedido_id>/', views.calificar_pedido, name='calificar_pedido'),
    
    # ============ CANCELACIÓN ============
    path('cancelar/<int:pedido_id>/', views.cancelar_pedido, name='cancelar_pedido'),
    
    # ============ HISTORIAL ============
    path('historial/', views.historial_pedidos, name='historial'),
]