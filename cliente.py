import os
import platform
import socket
import datetime
from prettytable import PrettyTable

MAX_BUFFER_SIZE = 1024

def enviar_mensaje(ip, puerto, mensaje):
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    respuesta = None

    try:
        # Conectar al servidor
        sock.connect((ip, puerto))

        # Enviar el mensaje al servidor
        sock.send(mensaje.encode())
        while True:
            # Recibir y mostrar la respuesta del servidor
            data = sock.recv(MAX_BUFFER_SIZE).decode()
            if data:
                respuesta = data
                break
            else:
                # Si no hay datos, el servidor ha cerrado la conexión
                break
    except socket.error as e:
        print("Error de socket:", e)
    finally:
        # Cerrar la conexión
        sock.close()
    
    return respuesta

def agregar_producto():
    limpiar_pantalla()
    
    print("\nAgregar Producto\n")

    nombre = input("Ingrese el nombre del producto: ")
    descripcion = input("Ingrese la descripción del producto: ")

    while True:
        precio = input("Ingrese el precio del producto: ")
        if precio.isdigit():
            break
        else:
            print("\nEl precio debe ser un número entero. Inténtelo de nuevo.")
    
    while True:
        stock = input("Ingrese el stock del producto: ")
        if stock.isdigit():
            break
        else:
            print("\nEl stock debe ser un número entero. Inténtelo de nuevo.")

    while True:
        fecha_vencimiento = input("Ingrese la fecha de vencimiento del producto (dd/mm/aaaa) o dejar en blanco: ")

        if fecha_vencimiento == '':
            fecha_vencimiento = '01/01/2000'
            break
        else:
            try:
                datetime.datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                break
            except ValueError:
                print("\nFormato de fecha incorrecto. Debe ser dd/mm/aaaa. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"gprodadd:{nombre}:{descripcion}:{precio}:{stock}:{fecha_vencimiento}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

def editar_producto():
    limpiar_pantalla()
    mensaje = "Editar producto"
    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)
    print("\nRespuesta del servidor:", respuesta)

def eliminar_producto():
    limpiar_pantalla()
    mensaje = "Eliminar producto"
    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)
    print("\nRespuesta del servidor:", respuesta)

def ver_producto_id():
    limpiar_pantalla()
    mensaje = "Ver producto por ID"

    mensaje_sin_tamaño = f"gprodlist"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    tabla = PrettyTable()
    tabla.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]


def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def registrar_venta():
    limpiar_pantalla()
    print("\nRegistrando Venta\n")

def ver_productos():
    limpiar_pantalla()
    print("\nViendo Productos\n")

def buscar_producto():
    limpiar_pantalla()
    print("\nBuscando Producto\n")

def ver_estadisticas():
    limpiar_pantalla()
    print("\nViendo Estadisticas\n")

def gestionar_productos():
    limpiar_pantalla()
    while True:
        print("---------- GESTIONAR PRODUCTOS ---------")
        print("|                                      |")
        print("|   1. Agregar Producto                |")
        print("|   2. Editar Producto                 |")
        print("|   3. Eliminar Producto               |")
        print("|   4. Ver Producto por ID             |")
        print("|   9. Volver al menú principal        |")
        print("|                                      |")
        print("----------------------------------------")

        opcion_producto = input("\nIngrese su opción: ")

        if opcion_producto == '1':
            agregar_producto()
        elif opcion_producto == '2':
            editar_producto()
        elif opcion_producto == '3':
            eliminar_producto()
        elif opcion_producto == '4':
            ver_producto_id()
        elif opcion_producto == '9':
            break
        else:
            print("\nEntrada no válida, intentelo de nuevo.")

        input("\nPresione Enter para continuar...")

def gestionar_categorias():
    limpiar_pantalla()
    print("\nGestionando Categorias\n")

def menu_principal():
    limpiar_pantalla()
    print("------------- MENU PRINCIPAL ------------")
    print("|                                      |")
    print("|   1. Registrar Venta                 |")
    print("|   2. Ver Productos                   |")
    print("|   3. Buscar Producto                 |")
    print("|   4. Ver estadisticas                |")
    print("|   5. Gestionar Productos             |")
    print("|   6. Gestionar Categorias            |")
    print("|   9. Salir                           |")
    print("|                                      |")
    print("----------------------------------------")

if __name__ == "__main__":
    while True:
        menu_principal()
        opcion = input("\nIngrese su opción: ")

        if opcion == '1':
            registrar_venta()
        elif opcion == '2':
            ver_productos()
        elif opcion == '3':
            buscar_producto()
        elif opcion == '4':
            ver_estadisticas()
        elif opcion == '5':
            gestionar_productos()
        elif opcion == '6':
            gestionar_categorias()
        elif opcion == '9':
            break
        else:
            print("\nEntrada no válida, intentelo de nuevo.")
        
        input("\nPresione Enter para continuar...")
