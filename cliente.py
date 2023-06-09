import time
import os
import platform
import socket
import re
from decimal import Decimal
from datetime import datetime
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
                datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                break
            except ValueError:
                print("\nFormato de fecha incorrecto. Debe ser dd/mm/aaaa. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"gprodadd:{nombre}:{descripcion}:{precio}:{stock}:{fecha_vencimiento}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    # # Agregar el producto al historial de precios
    # print(respuesta[39:])
    # producto_id = respuesta[39:]
    # mensaje_sin_tamaño_historial = f"geshiadd:{precio}:{producto_id}"
    # tamaño_mensaje_historial = f"{len(mensaje_sin_tamaño_historial):05d}"
    # mensaje_historial = tamaño_mensaje_historial + mensaje_sin_tamaño_historial
    # print("\nMensaje enviado al servidor:", mensaje_historial)

    # respuesta_historial = enviar_mensaje("127.0.0.1", 5000, mensaje_historial)
    # print("\nRespuesta del servidor:", respuesta_historial)

def editar_producto():
    limpiar_pantalla()
    
    print("\Editar Producto\n")
    while True:
        id = input("Ingrese el ID del producto: ")
        
        if id.isdigit():
            break
        else:
            print("\nEl id es obligatorio.")

    nombre = input("Ingrese el nombre del producto: ")
    if nombre == '':
        nombre = 'null'
    descripcion = input("Ingrese la descripción del producto: ")
    if descripcion == '':
        descripcion = 'null'

    while True:
        precio = input("Ingrese el precio del producto: ")
        
        if precio == '':
            precio = 'null'
            break
        elif precio.isdigit():
            break
        else:
            print("\nEl precio debe ser un número entero. Inténtelo de nuevo.")
    
    while True:
        stock = input("Ingrese el stock del producto: ")
        if stock == '':
            stock = 'null'
            break
        elif stock.isdigit():
            break
        else:
            print("\nEl stock debe ser un número entero. Inténtelo de nuevo.")

    while True:
        fecha_vencimiento = input("Ingrese la fecha de vencimiento del producto (dd/mm/aaaa): ")

        if fecha_vencimiento == '':
            fecha_vencimiento = 'null'
            break
        else:
            try:
                datetime.strptime(fecha_vencimiento, "%d/%m/%Y")
                break
            except ValueError:
                print("\nFormato de fecha incorrecto. Debe ser dd/mm/aaaa. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"gprodedit:{id}:{nombre}:{descripcion}:{precio}:{stock}:{fecha_vencimiento}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)
    print("\nRespuesta del servidor:", respuesta)

    # if precio != 'null':
    #     mensaje_sin_tamaño_historial = f"geshiadd:{precio}:{id}"
    #     tamaño_mensaje_historial = f"{len(mensaje_sin_tamaño_historial):05d}"
    #     mensaje_historial = tamaño_mensaje_historial + mensaje_sin_tamaño_historial
    #     print("\nMensaje enviado al servidor:", mensaje_historial)

    #     respuesta_historial = enviar_mensaje("127.0.0.1", 5000, mensaje_historial)
    #     print("\nRespuesta del servidor:", respuesta_historial)

def eliminar_producto():
    limpiar_pantalla()
    print("\Eliminar Producto\n")
    while True:
        id = input("Ingrese el ID del producto: ")
        if id.isdigit():
            break
        else:
            print("\nEl id es obligatorio.")

    mensaje_sin_tamaño = f"gproddel:{id}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño
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

    data_string = respuesta[12:]

    if data_string != ' Productos no fueron encontrados!':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), descripcion.strip("'"), Decimal(precio.strip("'")), int(stock), datetime.strptime(fecha.strip("'"), "%Y-%m-%d").date()) for id, nombre, descripcion, precio, stock, fecha in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]
        print("datitos ", tuplas)
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)

def obtener_stock_por_id(productos, id):
    for producto in productos:
        if producto[0] == id:
            return producto[4]  # Retornar el valor del stock (tercer elemento de la tupla)
    return None

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def registrar_venta():
    limpiar_pantalla()
    
    print("\nAgregar Venta\n")
    #Solo ingresar Fecha de la venta.
   
    while True:
        fecha_vendido = input("Ingrese la fecha de compra del producto (dd/mm/aaaa) o dejar en blanco si la venta es hoy: ")

        if fecha_vendido == '':
            fecha_vendido = datetime.now().strftime("%d/%m/%Y")
            print("Fecha de la Venta: ", fecha_vendido)
            break
        else:
            try:
                datetime.strptime(fecha_vendido, "%d/%m/%Y")
                print("Fecha de la Venta: ", fecha_vendido)
                break
            except ValueError:
                print("\nFormato de fecha incorrecto. Debe ser dd/mm/aaaa. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"gventaddVenta:{fecha_vendido}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"  #Esta parte no se que hace#
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)
    
    venta_id = respuesta[39:]
    print(venta_id)
    print("\nRegistrando Venta\n")

    while True:
        try:

            cantidad_prod = int(input("Ingrese la cantidad de tipos de productos vendidos: "))
            if cantidad_prod >= 0:
                break
            else:
                print("\nLa cantidad debe ser un número entero o mayor a 0. Inténtelo de nuevo.")
        except ValueError:
            print("\nValor invalido")
    
    limpiar_pantalla()
    
    detalles_ventas = []
    for i in range(cantidad_prod):

        # Mostrar la lista de productos existentes
        limpiar_pantalla()
        mensaje = "Ver producto por ID"

        mensaje_sin_tamaño = f"gprodlist"
        tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
        mensaje = tamaño_mensaje + mensaje_sin_tamaño

        print("\nMensaje enviado al servidor:", mensaje)

        respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

        print("\nRespuesta del servidor:", respuesta)

        data_string = respuesta[12:]

        if data_string != ' Productos no fueron encontrados!':
            data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
            data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

            # Eliminar los paréntesis y los espacios extra
            data_string = re.sub(r"[()]", "", data_string)
            data_string = re.sub(r"\s+", "", data_string)

            # Dividir la cadena por las comas para obtener una lista de elementos
            elementos = data_string.split(",")

            # Agrupar los elementos en tuplas de 6
            tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

            # Convertir los valores de cadena a los tipos de datos apropiados
            tuplas = [(int(id), nombre.strip("'"), descripcion.strip("'"), Decimal(precio.strip("'")), int(stock), datetime.strptime(fecha.strip("'"), "%Y-%m-%d").date()) for id, nombre, descripcion, precio, stock, fecha in tuplas]

            table = PrettyTable()

            # Añadir las columnas
            table.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]
            print("datitos ", tuplas)
            # Añadir las filas
            for row in tuplas:
                table.add_row(row)

            # Imprimir la tabla
            print(table)
            
            # Solicitar los detalles del producto
            while True:
                try:
                    id_producto = int(input("\nIngrese el ID del producto: "))
                    cantidad_producto = int(input("Ingrese la cantidad de este producto vendido: "))
                    precio_producto = float(input("Ingrese el precio de venta del producto: "))
                    break
                except ValueError:
                    print("Valor inválido. Intente nuevamente.")

            # Enviar los detalles de venta al servicio de gestión de ventas
            mensaje_sin_tamaño = f"gventaddDet:{venta_id},{id_producto},{cantidad_producto},{precio_producto}"
            tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
            mensaje = tamaño_mensaje + mensaje_sin_tamaño

            print("\nMensaje enviado al servidor:", mensaje)

            respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

            print("\nRespuesta del servidor:", respuesta)

            if respuesta.split(':')[0][12:] == '1':
                print("\Editar Producto\n")
                id = id_producto
                nombre = 'null'
                descripcion = 'null'
                precio = 'null'
                stock = obtener_stock_por_id(tuplas, id) - cantidad_producto
                fecha_vencimiento = 'null'
                mensaje_sin_tamaño = f"gprodedit:{id}:{nombre}:{descripcion}:{precio}:{stock}:{fecha_vencimiento}"
                tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
                mensaje = tamaño_mensaje + mensaje_sin_tamaño
                respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)
            
            time.sleep(2)


def ver_productos():
    limpiar_pantalla()
    print("\nViendo Productos\n")

def buscar_producto():
    limpiar_pantalla()

    print("\nBuscar Producto (ID o nombre)\n")
    while True:
        search = input("Ingrese producto: ")
        if search.isdigit() or search.isalpha():
            break
        else:
            print("\nEntrada incorrecta. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"buscabusca:{search}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    data_string = respuesta[12:]

    if data_string != ' Producto no encontrado!':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), descripcion.strip("'"), Decimal(precio.strip("'")), int(stock), datetime.strptime(fecha.strip("'"), "%Y-%m-%d").date()) for id, nombre, descripcion, precio, stock, fecha in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]
        print("datitos ", tuplas)
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)


def ver_estadisticas():
    limpiar_pantalla()

    print("\nViendo Estadisticas\n")
    
    while True:
        print("------------- ESTADÍSTICAS ------------")
        print("|                                      |")
        print("|   1. Ver producto menos vendido      |")
        print("|   2. Ver producto mas vendido        |")
        print("|   9. Salir                           |")
        print("|                                      |")
        print("----------------------------------------")

        opcion = input("\nIngrese su opción: ")

        if opcion == '1':
            productos_menos_vendidos()
        elif opcion == '2':
            productos_mas_vendidos()
        elif opcion == '9':
            break
        else:
            print("\nEntrada no válida, intentelo de nuevo.")
    
    input("\nPresione Enter para continuar...")



def productos_menos_vendidos():
    limpiar_pantalla()

    mensaje = "Ver producto menos vendido"

    mensaje_sin_tamaño = f"estadmenosVend"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    data_string = respuesta[12:]

    if data_string != ' Productos no fueron encontrados!':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        
        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        print(tuplas)
        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), total_vendido.strip("'")) for id, nombre, total_vendido in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre Producto", "Total vendido"]
        print("datitos ", tuplas)
        print("\nProductos menos vendidos\n")
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)

def  productos_mas_vendidos():
    limpiar_pantalla()

    mensaje = "Ver producto mas vendido"

    mensaje_sin_tamaño = f"estadmasVend"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    data_string = respuesta[12:]

    if data_string != ' Productos no fueron encontrados!':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        print(tuplas)
        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), total_vendido.strip("'")) for id, nombre, total_vendido in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre Producto", "Total vendido"]
        print("datitos ", tuplas)
        print("\nProductos mas vendidos\n")
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)

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
    while True:
        print("---------- GESTIONAR CATEGORIAS ---------")
        print("|                                      |")
        print("|   1. Agregar Categoria               |")
        print("|   2. Editar Categoria                |")
        print("|   3. Eliminar Categoria              |")
        print("|   4. Unir Categoria-Producto         |")
        print("|   9. Volver al menú principal        |")
        print("|                                      |")
        print("----------------------------------------")

        opcion_categoria = input("\nIngrese su opción: ")

        if opcion_categoria == '1':
            agregar_categoria()
        elif opcion_categoria == '2':
            editar_categoria()
        elif opcion_categoria == '3':
            eliminar_categoria()
        elif opcion_categoria == '4':
            unir_categoria_producto()
        elif opcion_categoria == '9':
            break
        else:
            print("\nEntrada no válida, intentelo de nuevo.")

        input("\nPresione Enter para continuar...")

def agregar_categoria():
    limpiar_pantalla()
    print("\nAgregar Categoria\n")
    
    while True:
        nombre = input("Ingrese el nombre de la categoria: ")
        if nombre.isalpha():
            break
        else:
            print("\nEl nombre debe ser una cadena de caracteres. Inténtelo de nuevo.")
    
    
    mensaje_sin_tamaño = f"gcateadd:{nombre}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)


def editar_categoria():
    limpiar_pantalla()
    print("\nEditar Categoria\n")
    while True:
        id= input("Ingrese el ID de la categoria: ")
        if id.isdigit():
            break
        else:
            print("\nEl ID debe ser un número. Inténtelo de nuevo.")

    while True:
        nombre = input("Ingrese el nombre de la categoria: ")
        if nombre.isalpha():
            break
        else:
            print("\nEl nombre debe ser una cadena de caracteres. Inténtelo de nuevo.")
            
    
    mensaje_sin_tamaño = f"gcateedit:{id}:{nombre}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

def eliminar_categoria():
    limpiar_pantalla()
    print("\nEliminar Categoria\n")
    while True:
        id = input("Ingrese el ID de la categoria: ")
        if id.isdigit():
            break
        else:
            print("\nEl id es obligatorio.")

    mensaje_sin_tamaño = f"gcatedel:{id}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño
    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)
    print("\nRespuesta del servidor:", respuesta)

def unir_categoria_producto():
    limpiar_pantalla()
    print("\nUnir Categoria-Prpoducto")
    while True:
        id_categoria = input("Ingrese el ID de la categoria: ")
        if id_categoria.isdigit():
            break
        else:
            print("\nEl id es obligatorio.")

    while True:
        id_producto = input("Ingrese el ID del producto: ")
        if id_producto.isdigit():
            break
        else:
            print("\nEl id es obligatorio.")
    
    mensaje_sin_tamaño = f"gcateunir:{id_categoria}:{id_producto}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño
    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

def productos_menos_stock():
    limpiar_pantalla()
    mensaje = "Producto con menos stock (10 unidades)"

    mensaje_sin_tamaño = f"stocklist"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    data_string = respuesta[12:]

    if data_string != ' No existen productos cerca a vencer (10 días)':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), descripcion.strip("'"), Decimal(precio.strip("'")), int(stock), datetime.strptime(fecha.strip("'"), "%Y-%m-%d").date()) for id, nombre, descripcion, precio, stock, fecha in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]
        print("datitos ", tuplas)
        print("\nProductos con menos stock (10 unidades)\n")
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)
    
def productos_cerca_vencer():
    limpiar_pantalla()
    mensaje = "Producto cerca a vencer (10 días)"

    mensaje_sin_tamaño = f"vencelist"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)
    
    data_string = respuesta[12:]

    if data_string != ' No existen productos cerca a vencer (10 días)':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), descripcion.strip("'"), Decimal(precio.strip("'")), int(stock), datetime.strptime(fecha.strip("'"), "%Y-%m-%d").date()) for id, nombre, descripcion, precio, stock, fecha in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Fecha de vencimiento"]
        print("datitos ", tuplas)
        print("\nProductos cerca a vencer (10 días)\n")

        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)

def historial_precios():
    limpiar_pantalla()

    print("\nHistorial de precios (por ID)\n")
    while True:
        search = input("Ingrese producto: ")
        if search.isdigit() and int(search) >= 0:
            break
        else:
            print("\nEntrada incorrecta. Inténtelo de nuevo.")

    mensaje_sin_tamaño = f"geshilist:{search}"
    tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
    mensaje = tamaño_mensaje + mensaje_sin_tamaño

    print("\nMensaje enviado al servidor:", mensaje)

    respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

    print("\nRespuesta del servidor:", respuesta)

    data_string = respuesta[12:]

    if data_string != ' Producto no encontrado!':
        data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
        data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

        # Eliminar los paréntesis y los espacios extra
        data_string = re.sub(r"[()]", "", data_string)
        data_string = re.sub(r"\s+", "", data_string)

        # Dividir la cadena por las comas para obtener una lista de elementos
        elementos = data_string.split(",")

        # Agrupar los elementos en tuplas de 6
        tuplas = [tuple(elementos[i:i+6]) for i in range(0, len(elementos), 6)]

        # Convertir los valores de cadena a los tipos de datos apropiados
        tuplas = [(int(id), nombre.strip("'"), Decimal(precio.strip("'"))) for id, nombre, precio in tuplas]

        table = PrettyTable()

        # Añadir las columnas
        table.field_names = ["ID", "Nombre", "Precio"]
        print("datitos ", tuplas)
        # Añadir las filas
        for row in tuplas:
            table.add_row(row)

        # Imprimir la tabla
        print(table)

def menu_principal():
    limpiar_pantalla()
    print("------------- MENU PRINCIPAL ------------")
    print(f"|          Bienvenido {datos['usuario']}  |")
    print("|                                      |")
    print("|   1. Registrar Venta                 |")
    print("|   2. Buscar Producto                 |")
    print("|   3. Ver estadisticas                |")
    print("|   4. Gestionar Productos             |")
    print("|   5. Gestionar Categorias            |")
    print("|   6. Productos con menos stock       |")
    print("|   7. Productos cerca a vencer        |")
    print("|   8. Historial de precios producto   |")
    print("|   9. Salir                           |")
    print("|                                      |")
    print("----------------------------------------")

if __name__ == "__main__":

    datos = {}

    while True:

        # Ingresar al sistema con un usuario y contraseña válidos
        while True:
            limpiar_pantalla()
            print("------------- LOGIN ------------")
            print("|                             |")
            print("|   1. Ingresar al sistema    |")
            print("|   2. Salir                  |")
            print("|                             |")
            print("--------------------------------")

            opcion_login = input("\nIngrese su opción: ")

            if opcion_login == '1':
                break
            elif opcion_login == '2':
                exit()
            else:
                print("\nEntrada no válida, intentelo de nuevo.")

        while True:

            limpiar_pantalla()
            print("------------- LOGIN ------------")
            print("|                             |")
            print("|   Ingrese sus credenciales  |")
            print("|                             |")
            print("--------------------------------")

            usuario = input("\nUsuario: ")
            contraseña = input("Contraseña: ")

            mensaje_sin_tamaño = f"logjuvalida:{usuario},{contraseña}"
            tamaño_mensaje = f"{len(mensaje_sin_tamaño):05d}"
            mensaje = tamaño_mensaje + mensaje_sin_tamaño

            print("\nMensaje enviado al servidor:", mensaje)

            respuesta = enviar_mensaje("127.0.0.1", 5000, mensaje)

            print("\nRespuesta del servidor:", respuesta)

            if respuesta.split(':')[0][12:] == '1':
                data_string = respuesta.split(':')[1]
                data_string = re.sub(r"Decimal\('(\d+\.\d+)'\)", r"'\1'", data_string)
                data_string = re.sub(r"datetime\.date\((\d+), (\d+), (\d+)\)", r"'\1-\2-\3'", data_string)

                # Eliminar los paréntesis y los espacios extra
                data_string = re.sub(r"[()]", "", data_string)
                data_string = re.sub(r"\s+", "", data_string)

                # Dividir la cadena por las comas para obtener una lista de elementos
                elementos = data_string.split(",")
                print("\nCredenciales correctas.")
                datos['id'] = elementos[0]
                datos['usuario'] = elementos[1]
                datos['tienda_id'] = elementos[2]
                time.sleep(3)
                break
            # datos['id'] = '1'
            # datos['usuario'] = 'elementos[1]'
            # datos['tienda_id'] = 'elementos[2]'

            # break
            else:
                print("\nCredenciales incorrectas. Inténtelo de nuevo.")
                time.sleep(3)

        while True :
            menu_principal()
            opcion = input("\nIngrese su opción: ")

            if opcion == '1':
                registrar_venta()
            elif opcion == '2':
                buscar_producto()
            elif opcion == '3':
                ver_estadisticas()
            elif opcion == '4':
                gestionar_productos()
            elif opcion == '5':
                gestionar_categorias()
            elif opcion == '6':
                productos_menos_stock()
            elif opcion == '7':
                productos_cerca_vencer()
            elif opcion == '8':
                historial_precios()
            elif opcion == '9':
                break
            else:
                print("\nEntrada no válida, intentelo de nuevo.")
            
            input("\nPresione Enter para continuar...")
