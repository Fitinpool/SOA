import socket
import mysql.connector
from datetime import datetime 

MAX_BUFFER_SIZE = 1024

def generar_codigo(cadena):
    cantidad = len(cadena)
    cantidad_str = str(cantidad).zfill(5)
    return cantidad_str

def procesar_mensaje(data_mensaje, sock):
    # Removiendo espacios al inicio y al final
    # data_mensaje = data_mensaje.strip()

    # Data
    data = data_mensaje[5:]

    print("Data:", data)

    # Procesar la data
    tokens = data.split(":")

    print(tokens)

    

    if tokens[0] == 'add':
        # 00060gprodadd:polera:lindo producto para los niños:1000:100:null:1
        # 00052gprodadd:manzana:ilustre manzana:2000:50:10/12/2023:1
        variables = (tokens[1], tokens[2], tokens[3], tokens[4], datetime.strptime(tokens[5], '%d/%m/%Y').date() if tokens[5] != 'null' else None, tokens[6])
        print(variables)
        # Consulta SQL
        query = ("INSERT INTO Productos (nombre, descripcion, precio, stock, fecha_vencimiento, categoria_id) VALUES (%s,%s,%s,%s,%s,%s)")

        mensaje = 'dbges1:' + query + ':' + str(variables)

        mensaje = generar_codigo(mensaje) + mensaje

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
                data = data_mensaje[5:]
                if data == '1':
                    print("Producto agregado.")
                    newData = f'gprod Producto {tokens[1]} Agregado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Producto no agregado.")
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'delete':
         # 00013gproddelete:5
        variables = (tokens[1], )
        # Consulta SQL
        nombre = ejecutar_consulta_sql(("SELECT nombre FROM Productos WHERE id=%s"), variables)
        query = ("DELETE FROM Productos WHERE id=%s")
        
        resultados = ejecutar_consulta_sql(query, variables)
        print(resultados.rowcount, " producto eliminado.")
        if resultados.rowcount > 0:
            newData = f'gprod Producto {nombre.fetchall()[0][0]} - {tokens[1]} Eliminado!'
            sock.send(('000'+ str(len(newData)) + newData).encode())

    elif tokens[0] == 'edit':
        # 00061gprodedit:9:manzana:editando la manzanita:2000:50:10/12/2023:1
        variables = (tokens[2], tokens[3], tokens[4], tokens[5], datetime.strptime(tokens[6], '%d/%m/%Y').date() if tokens[6] != 'null' else None, tokens[7], tokens[1])
        # Consulta SQL
        query = ("UPDATE Productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, fecha_vencimiento = %s, categoria_id = %s WHERE id = %s")


        resultados = ejecutar_consulta_sql(query, variables)
        print(resultados.rowcount, " producto editado.")
        if resultados.rowcount > 0:
            newData = f'gprod Producto {tokens[2]} - {tokens[1]} Editado!'
            sock.send(('000'+ str(len(newData)) + newData).encode())


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
    mensaje = "00010sinitgprod"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
