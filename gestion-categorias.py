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
        variables = str(tokens[1]) 

        # Consulta SQL
        query = ("INSERT INTO Categorias (nombre) VALUES (%s);")

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
                    print("Categoria agregada.")
                    newData = f'gcate Categoria {tokens[1]} Agregada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Categoria no agregado.")
                    newData = f'gcate Categoria {tokens[1]} no fue agregada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'del':
         # 00014gproddelete:10
        variables = str(tokens[1])
        # Consulta SQL
        query = ("DELETE FROM Categorias WHERE id=%s;")
        
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
                    print("Categoria eliminada.")
                    newData = f'gcate Categorias {tokens[1]} eliminada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Categoria no eliminada.")
                    newData = f'gcate Categorias no {tokens[1]} eliminada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'edit':
        variables = str(tokens[2]) + ',' + str(tokens[1]) 
        # Consulta SQL
        query = "UPDATE Categorias SET nombre = %s WHERE id = %s;"

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
                data = data[7:]
                if data.split(":")[0] == '1':
                    print("Categoria editada.")
                    newData = f'gcate Categoria {tokens[1]} editada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Categoria no eliminado.")
                    newData = f'gcate Categoria {tokens[1]} no editada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break
    
    elif tokens[0] == 'unir':
        # 00060gprodedit:11:1
        variables = str(tokens[1]) + ',' + str(tokens[2]) 

        query = "INSERT INTO Categoria_Producto (categoria_id, producto_id) VALUES (%s,%s);"

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
                data = data[7:]

                if data.split(":")[0] == '1':
                    print("Se agregó la categoria al producto.")
                    newData = f'gcate Categoria {tokens[1]} añadida!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Categoria no Unida")
                    newData = f'gcate Categoria no {tokens[1]} añadida!'
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
    mensaje = "00010sinitgcate"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
