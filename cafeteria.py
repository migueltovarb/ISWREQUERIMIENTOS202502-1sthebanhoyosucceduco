import json
import os
from typing import Dict, List

class Cafeteria:
    def __init__(self):
        self.menu_file = "menu.json"
        self.menu = self.cargar_menu()
        self.pedido = {}
        
    def cargar_menu(self) -> Dict:
        """Carga el menú desde un archivo JSON o crea uno por defecto"""
        if os.path.exists(self.menu_file):
            try:
                with open(self.menu_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.menu_por_defecto()
        else:
            menu_default = self.menu_por_defecto()
            self.guardar_menu(menu_default)
            return menu_default
    
    def menu_por_defecto(self) -> Dict:
        """Menú inicial por defecto"""
        return {
            "Café Americano": {"precio": 3500, "cantidad": 50},
            "Café con Leche": {"precio": 4000, "cantidad": 40},
            "Cappuccino": {"precio": 4500, "cantidad": 30},
            "Latte": {"precio": 5000, "cantidad": 25},
            "Espresso": {"precio": 3000, "cantidad": 60},
            "Té Verde": {"precio": 3000, "cantidad": 20},
            "Chocolate Caliente": {"precio": 4200, "cantidad": 15},
            "Croissant": {"precio": 2800, "cantidad": 30},
            "Muffin": {"precio": 3200, "cantidad": 20},
            "Sandwich": {"precio": 6500, "cantidad": 15}
        }
    
    def guardar_menu(self, menu: Dict = None):
        """Guarda el menú en un archivo JSON"""
        menu_a_guardar = menu if menu else self.menu
        with open(self.menu_file, 'w', encoding='utf-8') as f:
            json.dump(menu_a_guardar, f, indent=4, ensure_ascii=False)
    
    def mostrar_menu(self):
        """Muestra el menú completo con precios"""
        print("\n" + "="*50)
        print("           MENÚ DE LA CAFETERÍA")
        print("="*50)
        print(f"{'ID':<3} {'PRODUCTO':<20} {'PRECIO':<10} {'DISPONIBLE'}")
        print("-"*50)
        
        for i, (producto, info) in enumerate(self.menu.items(), 1):
            precio_formateado = f"${info['precio']:,}"
            disponible = "Sí" if info['cantidad'] > 0 else "No"
            print(f"{i:<3} {producto:<20} {precio_formateado:<10} {disponible}")
        print("="*50)
    
    def realizar_pedido(self):
        """Proceso completo para realizar un pedido"""
        print("\n🛒 REALIZAR PEDIDO")
        
        while True:
            self.mostrar_menu()
            print("\nOpciones:")
            print("1. Agregar producto al pedido")
            print("2. Ver pedido actual")
            print("3. Editar pedido")
            print("4. Finalizar pedido")
            print("5. Cancelar pedido")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.agregar_al_pedido()
            elif opcion == "2":
                self.mostrar_pedido_actual()
            elif opcion == "3":
                self.editar_pedido()
            elif opcion == "4":
                if self.finalizar_pedido():
                    break
            elif opcion == "5":
                if self.cancelar_pedido():
                    break
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def agregar_al_pedido(self):
        """Agregar un producto al pedido"""
        try:
            producto_id = int(input("\nIngrese el ID del producto: ")) - 1
            productos = list(self.menu.keys())
            
            if 0 <= producto_id < len(productos):
                producto = productos[producto_id]
                info = self.menu[producto]
                
                if info['cantidad'] <= 0:
                    print(f"❌ {producto} no está disponible")
                    return
                
                print(f"Producto seleccionado: {producto} - ${info['precio']:,}")
                cantidad = int(input("Cantidad deseada: "))
                
                if cantidad <= 0:
                    print("❌ La cantidad debe ser mayor a 0")
                    return
                
                if cantidad > info['cantidad']:
                    print(f"❌ Solo hay {info['cantidad']} unidades disponibles")
                    return
                
                if producto in self.pedido:
                    nueva_cantidad = self.pedido[producto]['cantidad'] + cantidad
                    if nueva_cantidad > info['cantidad']:
                        print(f"❌ Cantidad total excede el stock disponible ({info['cantidad']})")
                        return
                    self.pedido[producto]['cantidad'] = nueva_cantidad
                else:
                    self.pedido[producto] = {
                        'precio': info['precio'],
                        'cantidad': cantidad
                    }
                
                print(f"✅ {cantidad} {producto}(s) agregado(s) al pedido")
            else:
                print("❌ ID de producto no válido")
        except ValueError:
            print("❌ Por favor ingrese números válidos")
    
    def mostrar_pedido_actual(self):
        """Muestra el pedido actual"""
        if not self.pedido:
            print("\n📝 Tu pedido está vacío")
            return
        
        print("\n" + "="*40)
        print("        TU PEDIDO ACTUAL")
        print("="*40)
        total = 0
        
        for i, (producto, info) in enumerate(self.pedido.items(), 1):
            subtotal = info['precio'] * info['cantidad']
            total += subtotal
            print(f"{i}. {producto}")
            print(f"   Cantidad: {info['cantidad']} x ${info['precio']:,} = ${subtotal:,}")
        
        print("-"*40)
        print(f"TOTAL: ${total:,}")
        print("="*40)
    
    def editar_pedido(self):
        """Permite editar el pedido actual"""
        if not self.pedido:
            print("\n📝 No hay productos en el pedido")
            return
        
        while True:
            self.mostrar_pedido_actual()
            print("\nOpciones de edición:")
            print("1. Agregar más cantidad a un producto")
            print("2. Reducir cantidad de un producto")
            print("3. Quitar producto del pedido")
            print("0. Volver")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.modificar_cantidad_pedido("agregar")
            elif opcion == "2":
                self.modificar_cantidad_pedido("reducir")
            elif opcion == "3":
                self.quitar_del_pedido()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def modificar_cantidad_pedido(self, accion: str):
        """Modifica la cantidad de un producto en el pedido"""
        try:
            producto_id = int(input("Ingrese el número del producto: ")) - 1
            productos_pedido = list(self.pedido.keys())
            
            if 0 <= producto_id < len(productos_pedido):
                producto = productos_pedido[producto_id]
                cantidad_actual = self.pedido[producto]['cantidad']
                cantidad_cambio = int(input(f"Cantidad a {'agregar' if accion == 'agregar' else 'reducir'}: "))
                
                if cantidad_cambio <= 0:
                    print("❌ La cantidad debe ser mayor a 0")
                    return
                
                if accion == "agregar":
                    nueva_cantidad = cantidad_actual + cantidad_cambio
                    if nueva_cantidad > self.menu[producto]['cantidad']:
                        print(f"❌ No hay suficiente stock. Disponible: {self.menu[producto]['cantidad']}")
                        return
                    self.pedido[producto]['cantidad'] = nueva_cantidad
                    print(f"✅ Se agregaron {cantidad_cambio} unidades")
                
                else:  # reducir
                    nueva_cantidad = cantidad_actual - cantidad_cambio
                    if nueva_cantidad <= 0:
                        del self.pedido[producto]
                        print(f"✅ {producto} removido del pedido")
                    else:
                        self.pedido[producto]['cantidad'] = nueva_cantidad
                        print(f"✅ Se redujeron {cantidad_cambio} unidades")
            else:
                print("❌ Número de producto no válido")
        except ValueError:
            print("❌ Por favor ingrese números válidos")
    
    def quitar_del_pedido(self):
        """Quita un producto completo del pedido"""
        try:
            producto_id = int(input("Ingrese el número del producto a quitar: ")) - 1
            productos_pedido = list(self.pedido.keys())
            
            if 0 <= producto_id < len(productos_pedido):
                producto = productos_pedido[producto_id]
                del self.pedido[producto]
                print(f"✅ {producto} removido del pedido")
            else:
                print("❌ Número de producto no válido")
        except ValueError:
            print("❌ Por favor ingrese un número válido")
    
    def finalizar_pedido(self) -> bool:
        """Finaliza el pedido y muestra resumen"""
        if not self.pedido:
            print("\n❌ No hay productos en el pedido")
            return False
        
        print("\n" + "="*50)
        print("           RESUMEN FINAL DEL PEDIDO")
        print("="*50)
        
        total = 0
        for producto, info in self.pedido.items():
            subtotal = info['precio'] * info['cantidad']
            total += subtotal
            print(f"{producto}")
            print(f"  Cantidad: {info['cantidad']} x ${info['precio']:,} = ${subtotal:,}")
        
        print("-"*50)
        print(f"TOTAL A PAGAR: ${total:,}")
        print("="*50)
        
        confirmacion = input("\n¿Confirmar pedido? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Actualizar inventario
            for producto, info in self.pedido.items():
                self.menu[producto]['cantidad'] -= info['cantidad']
            
            self.guardar_menu()
            print("✅ ¡Pedido confirmado! Gracias por su compra")
            self.pedido = {}
            input("\nPresione Enter para continuar...")
            return True
        else:
            print("❌ Pedido no confirmado")
            return False
    
    def cancelar_pedido(self) -> bool:
        """Cancela el pedido actual"""
        if not self.pedido:
            print("\n📝 No hay pedido que cancelar")
            return False
        
        confirmacion = input("\n¿Está seguro de cancelar el pedido? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            self.pedido = {}
            print("✅ Pedido cancelado")
            return True
        else:
            print("❌ Cancelación abortada")
            return False

class AdminCafeteria(Cafeteria):
    def __init__(self):
        super().__init__()
    
    def menu_administrador(self):
        """Menú principal del administrador"""
        while True:
            print("\n" + "="*40)
            print("      PANEL DE ADMINISTRADOR")
            print("="*40)
            print("1. Ver menú actual")
            print("2. Agregar nuevo producto")
            print("3. Quitar producto")
            print("4. Modificar precio")
            print("5. Modificar cantidad disponible")
            print("0. Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.mostrar_menu()
                input("\nPresione Enter para continuar...")
            elif opcion == "2":
                self.agregar_producto()
            elif opcion == "3":
                self.quitar_producto()
            elif opcion == "4":
                self.modificar_precio()
            elif opcion == "5":
                self.modificar_cantidad()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def agregar_producto(self):
        """Agrega un nuevo producto al menú"""
        nombre = input("\nNombre del nuevo producto: ").strip()
        
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return
        
        if nombre in self.menu:
            print("❌ El producto ya existe en el menú")
            return
        
        try:
            precio = int(input("Precio del producto: $"))
            cantidad = int(input("Cantidad inicial: "))
            
            if precio <= 0 or cantidad < 0:
                print("❌ El precio debe ser mayor a 0 y la cantidad no puede ser negativa")
                return
            
            self.menu[nombre] = {"precio": precio, "cantidad": cantidad}
            self.guardar_menu()
            print(f"✅ Producto '{nombre}' agregado exitosamente")
            
        except ValueError:
            print("❌ Por favor ingrese números válidos")
    
    def quitar_producto(self):
        """Quita un producto del menú"""
        self.mostrar_menu()
        
        try:
            producto_id = int(input("\nIngrese el ID del producto a quitar: ")) - 1
            productos = list(self.menu.keys())
            
            if 0 <= producto_id < len(productos):
                producto = productos[producto_id]
                confirmacion = input(f"¿Está seguro de quitar '{producto}'? (s/n): ").strip().lower()
                
                if confirmacion == 's':
                    del self.menu[producto]
                    self.guardar_menu()
                    print(f"✅ Producto '{producto}' eliminado")
                else:
                    print("❌ Operación cancelada")
            else:
                print("❌ ID de producto no válido")
                
        except ValueError:
            print("❌ Por favor ingrese un número válido")
    
    def modificar_precio(self):
        """Modifica el precio de un producto"""
        self.mostrar_menu()
        
        try:
            producto_id = int(input("\nIngrese el ID del producto: ")) - 1
            productos = list(self.menu.keys())
            
            if 0 <= producto_id < len(productos):
                producto = productos[producto_id]
                precio_actual = self.menu[producto]['precio']
                print(f"Precio actual de '{producto}': ${precio_actual:,}")
                
                nuevo_precio = int(input("Nuevo precio: $"))
                
                if nuevo_precio <= 0:
                    print("❌ El precio debe ser mayor a 0")
                    return
                
                self.menu[producto]['precio'] = nuevo_precio
                self.guardar_menu()
                print(f"✅ Precio de '{producto}' actualizado a ${nuevo_precio:,}")
            else:
                print("❌ ID de producto no válido")
                
        except ValueError:
            print("❌ Por favor ingrese números válidos")
    
    def modificar_cantidad(self):
        """Modifica la cantidad disponible de un producto"""
        self.mostrar_menu()
        
        try:
            producto_id = int(input("\nIngrese el ID del producto: ")) - 1
            productos = list(self.menu.keys())
            
            if 0 <= producto_id < len(productos):
                producto = productos[producto_id]
                cantidad_actual = self.menu[producto]['cantidad']
                print(f"Cantidad actual de '{producto}': {cantidad_actual}")
                
                nueva_cantidad = int(input("Nueva cantidad: "))
                
                if nueva_cantidad < 0:
                    print("❌ La cantidad no puede ser negativa")
                    return
                
                self.menu[producto]['cantidad'] = nueva_cantidad
                self.guardar_menu()
                print(f"✅ Cantidad de '{producto}' actualizada a {nueva_cantidad}")
            else:
                print("❌ ID de producto no válido")
                
        except ValueError:
            print("❌ Por favor ingrese números válidos")

def menu_principal():
    """Menú principal del sistema"""
    cafeteria = Cafeteria()
    admin = AdminCafeteria()
    
    while True:
        print("\n" + "="*50)
        print("          ☕ SISTEMA DE CAFETERÍA ☕")
        print("="*50)
        print("1. 👤 Cliente - Realizar pedido")
        print("2. 👨‍💼 Administrador")
        print("3. 📋 Ver menú")
        print("0. 🚪 Salir")
        
        opcion = input("\nSeleccione su opción: ").strip()
        
        if opcion == "1":
            cafeteria.realizar_pedido()
        elif opcion == "2":
            # En una aplicación real, aquí habría autenticación
            password = input("Ingrese la contraseña de administrador: ")
            if password == "admin123":  # Contraseña simple para demostración
                admin.menu_administrador()
            else:
                print("❌ Contraseña incorrecta")
        elif opcion == "3":
            cafeteria.mostrar_menu()
            input("\nPresione Enter para continuar...")
        elif opcion == "0":
            print("\n¡Gracias por usar nuestro sistema! ☕")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n¡Hasta luego! ☕")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, reinicie el programa")