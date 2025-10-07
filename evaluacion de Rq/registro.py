__author__="Stheban Danilo Hoyos Villota"
__license__="GPL"
__version__="1.0.0"
__email__="stheban.hoyos@campusucc.edu.co"


# Inicializamos el diccionario de contactos
contactos = {}

def registrar_contacto():
    """Registra un nuevo contacto en la agenda."""
    nombre = input("Ingresa el nombre del contacto: ")
    # Verificamos si el contacto ya existe
    if nombre in contactos:
        print("¡Error! Ya existe un contacto con ese nombre.")
        return
    
    numero = input("Ingresa el número de teléfono: ")
    correo = input("Ingresa el correo electrónico: ")
    cargo = input("Ingresa el cargo en la empresa: ")
    
    # Creamos un diccionario para los detalles del contacto
    contactos[nombre] = {
        'numero': numero,
        'correo': correo,
        'cargo': cargo
    }
    print(f"Contacto '{nombre}' registrado exitosamente.")

def eliminar_contacto():
    """Elimina un contacto existente de la agenda."""
    nombre = input("Ingresa el nombre del contacto a eliminar: ")
    if nombre in contactos:
        del contactos[nombre] # Usamos 'del' para eliminar la clave
        print(f"Contacto '{nombre}' eliminado exitosamente.")
    else:
        print("¡Error! El contacto no existe.")

def eliminar_contacto_terminal():
    """Elimina un contacto mostrando la lista y seleccionando por número."""
    if not contactos:
        print("No hay contactos registrados.")
        return
    print("--- Eliminar Contacto ---")
    nombres = list(contactos.keys())
    for idx, nombre in enumerate(nombres, 1):
        print(f"{idx}. {nombre}")
    try:
        seleccion = int(input("Selecciona el número del contacto a eliminar: "))
        if 1 <= seleccion <= len(nombres):
            nombre = nombres[seleccion - 1]
            del contactos[nombre]
            print(f"Contacto '{nombre}' eliminado exitosamente.")
        else:
            print("Selección no válida.")
    except ValueError:
        print("Entrada no válida. Debe ser un número.")

def actualizar_contacto():
    """Actualiza la información de un contacto existente."""
    nombre = input("Ingresa el nombre del contacto a actualizar: ")
    if nombre in contactos:
        print(f"Datos actuales de '{nombre}': {contactos[nombre]}")
        print("Ingresa los nuevos datos (deja en blanco para mantener el actual):")
        
        nuevo_numero = input(f"Nuevo número ({contactos[nombre]['numero']}): ")
        if nuevo_numero:
            contactos[nombre]['numero'] = nuevo_numero
        
        nuevo_correo = input(f"Nuevo correo ({contactos[nombre]['correo']}): ")
        if nuevo_correo:
            contactos[nombre]['correo'] = nuevo_correo
            
        nuevo_cargo = input(f"Nuevo cargo ({contactos[nombre]['cargo']}): ")
        if nuevo_cargo:
            contactos[nombre]['cargo'] = nuevo_cargo
        
        print(f"Contacto '{nombre}' actualizado exitosamente.")
    else:
        print("¡Error! El contacto no existe.")

def mostrar_contactos():
    """Muestra todos los contactos registrados."""
    if not contactos:
        print("No hay contactos registrados.")
        return
    
    print("--- Lista de Contactos ---")
    for nombre, datos in contactos.items():
        print(f"Nombre: {nombre}")
        print(f"  - Número: {datos['numero']}")
        print(f"  - Correo: {datos['correo']}")
        print(f"  - Cargo: {datos['cargo']}")
        print("-" * 25)

def listar_contactos():
    """Muestra solo los nombres de todos los contactos registrados."""
    if not contactos:
        print("No hay contactos registrados.")
        return
    print("--- Nombres de Contactos ---")
    for nombre in contactos:
        print(nombre)
    print("-" * 25)

def buscar_contacto():
    """Busca un contacto por nombre y muestra sus datos si existe."""
    nombre = input("Ingresa el nombre del contacto a buscar: ")
    if nombre in contactos:
        datos = contactos[nombre]
        print(f"Nombre: {nombre}")
        print(f"  - Número: {datos['numero']}")
        print(f"  - Correo: {datos['correo']}")
        print(f"  - Cargo: {datos['cargo']}")
    else:
        print("¡Error! El contacto no existe.")

def menu():
    """Función principal para el menú de opciones."""
    while True:
        print("\n  Gestión de Contactos ")
        print("1. Registrar contacto")
        print("2. Eliminar contacto")
        print("3. Eliminar contacto (selección por número)")
        print("4. Actualizar contacto")
        print("5. Mostrar todos los contactos")
        print("6. Listar nombres de contactos")
        print("7. Buscar contacto")
        print("8. Salir")
        
        opcion = input("Selecciona una opción (1-8): ")
        
        if opcion == '1':
            registrar_contacto()
        elif opcion == '2':
            eliminar_contacto()
        elif opcion == '3':
            eliminar_contacto_terminal()
        elif opcion == '4':
            actualizar_contacto()
        elif opcion == '5':
            mostrar_contactos()
        elif opcion == '6':
            listar_contactos()
        elif opcion == '7':
            buscar_contacto()
        elif opcion == '8':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

# Ejecutamos el menú principal
if __name__ == "__main__":
    menu()
