import socket
import mysql.connector
from datetime import datetime 

MAX_BUFFER_SIZE = 1024

def generar_codigo(cadena):
    cantidad = len(cadena)
    cantidad_str = str(cantidad).zfill(5)
    return cantidad_str

def ejecutar_consulta_sql(consulta, variables):
    # Establecer la conexión a la base de datos
    conexion = mysql.connector.connect(
        host='localhost',
        port=1313,
        user='root',
        password='root',
        database='gestion_tienda',
        buffered=True
    )

    try:
        # Crear un cursor para ejecutar la consulta
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL
        cursor.execute(consulta, variables)

        # Obtener los resultados de la consulta
        resultados = cursor

        conexion.commit()
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

        # Devolver los resultados
        print(resultados)
        return resultados

    except mysql.connector.Error as error:
        print("Error al ejecutar la consulta SQL:", error)
        return []  # Devuelve una lista vacía en caso de error

def procesar_mensaje(data_mensaje, sock):
    # Removiendo espacios al inicio y al final
    # data_mensaje = data_mensaje.strip()

    # Data
    data = data_mensaje[5:]

    print("Data:", data)

    # Procesar la data
    tokens = data.split(":")

    print(tokens)
    if tokens[0] == '1' : 
        # 00151dbges1:INSERT INTO Productos (nombre, descripcion, precio, stock, fecha_vencimiento) VALUES (%s,%s,%s,%s,%s):manzana,ilustre manzana,2000,50,2023-12-10
        
        consulta = tokens[1]

        variables = tuple(tokens[2].split(","))

        res = ejecutar_consulta_sql((consulta), variables)

        print(res)
        if res.rowcount > 0:
            print(res.fetchall())
            newData = f'dbges1'
            sock.send((generar_codigo(newData) + newData).encode())
        else:
            newData = f'dbges0'
            sock.send((generar_codigo(newData) + newData).encode())
    elif tokens[0] == '0':
        consulta = tokens[1]

        res = ejecutar_consulta_sql(consulta, None)

        print(res)
        if res.rowcount > 0:
            newData = f'dbges1'
            sock.send((generar_codigo(newData) + newData).encode())
        else:
            newData = f'dbges0'
            sock.send((generar_codigo(newData) + newData).encode())



def enviar_mensaje(ip, puerto, mensaje):
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conectar al servidor
    sock.connect((ip, puerto))
    
    # Enviar el mensaje al servidor
    sock.send(mensaje.encode())
    
    while True:
        # Recibir y procesar las respuestas del servidor
        amount_received = 0
        amount_expected = int(sock.recv (5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len (data)
        
        data = data.decode()
        
        if data:
            print("Respuesta recibida:", data)
            procesar_mensaje(data, sock)
        else:
            print("Conexión cerrada por el servidor.")
            break

    # Cerrar la conexión
    sock.close()

def main():
    ip = "127.0.0.1"  # Dirección IP del servidor local
    puerto = 5000  # Puerto del servidor local
    mensaje = "00010sinitdbges"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
