import socket
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

    if tokens[0] == 'add':
        # 00058gprodadd:polera:lindo producto para los niños:1000:100:null
        # 00050gprodadd:manzana:ilustre manzana:2000:50:10/12/2023
        variables = str(tokens[1]) + ',' + str(tokens[2]) + ',' + str(tokens[3]) + ',' + str(tokens[4])  + ',' + str(datetime.strptime(tokens[5], '%d/%m/%Y').date())

        # Consulta SQL
        query = ("INSERT INTO Productos (nombre, descripcion, precio, stock, fecha_vencimiento) VALUES (%s,%s,%s,%s,%s)")

        mensaje = 'dbges0:' + query + ':' + variables

        mensaje = generar_codigo(mensaje) + mensaje
        print(mensaje)
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
                data = data[7:]
                print("SOY LA DATA DE RESPUESTA : ",data)
                if data.split(':')[0] == '1':
                    print("Producto agregado.")
                    newData = f'gprod Producto {tokens[1]} Agregado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Producto no agregado.")
                    newData = f'gprod Producto {tokens[1]} no fue agregado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'del':
         # 00014gproddelete:10
        variables = str(tokens[1])
        # Consulta SQL
        query = ("DELETE FROM Productos WHERE id=%s")
        
        mensaje = 'dbges0:' + query + ':' + variables

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
                print(data)
                data = data[7:]

                if data.split(":")[0] == '1':
                    print("Producto eliminado.")
                    newData = f'gprod Producto {tokens[1]} eliminado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Producto no eliminado.")
                    newData = f'gprod Producto no {tokens[1]} eliminado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'edit':
        # 00060gprodedit:11:manzana:editando la manzanita:2000:50:10/12/2023
        variables = ''
        query = "UPDATE Productos SET "
        for x in range(2, len(tokens)):
            if tokens[x] != 'null':
                variables += str(tokens[x]) + ','
                if x == 2:
                    query += "nombre = %s,"
                elif x == 3:
                    query += "descripcion = %s,"
                elif x == 4:
                    query += "precio = %s,"
                elif x == 5:
                    query += "stock = %s,"
                elif x == 6:
                    query += "fecha_vencimiento = %s,"

        if query.endswith(","):
            query = query[:-1]

        variables += str(tokens[1]) 
        query += " WHERE id = %s;"
        
        # Consulta SQL
        query = (query)

        mensaje = 'dbges0:' + query + ':' + variables

        print(mensaje)
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
                data = data[7:]

                if data.split(":")[0] == '1':
                    print("Producto editado.")
                    newData = f'gprod Producto {tokens[1]} editado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Producto no eliminado.")
                    newData = f'gprod Producto no {tokens[1]} editado!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break
    
    elif tokens[0] == 'list':
        # 00060gprodedit:11:manzana:editando la manzanita:2000:50:10/12/2023
        
        query = ("SELECT * FROM Productos;")

        mensaje = 'dbges1:' + query

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
                data = data[7:].split(':')
                print(data)
                if data[0] == '1':
                    print("Productos Encontrados.")
                    newData = f'gprod{data[1]}'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break
    else:
        print("Sin procesar.")
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
