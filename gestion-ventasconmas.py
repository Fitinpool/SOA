import socket
from datetime import datetime

MAX_BUFFER_SIZE = 1024

def generar_codigo(cadena):
    cantidad = len(cadena)
    cantidad_str = str(cantidad).zfill(5)
    return cantidad_str

def procesar_mensaje(data_mensaje, sock):
    data = data_mensaje[5:]

    print("Data:", data)

    tokens = data.split(":")

    if tokens[0] == 'add':
        variables = str(tokens[1]) + ',' + str(tokens[2]) + ',' + str(tokens[3]) + ',' + str(datetime.strptime(tokens[4], '%Y-%m-%d').date())

        query = ("INSERT INTO Ventas (producto, cantidad, precio, fecha_venta) VALUES (%s,%s,%s,%s)")

        mensaje = 'dbges0:' + query + ':' + variables

        mensaje = generar_codigo(mensaje) + mensaje
        print(mensaje)
        sock.send(mensaje.encode())

        while True:
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            data = data.decode()

            if data:
                data = data[7:]
                print("SOY LA DATA DE RESPUESTA:", data)
                if data.split(':')[0] == '1':
                    print("Venta agregada.")
                    newData = f'gvent Venta de {tokens[1]} agregada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Venta no agregada.")
                    newData = f'gvent Venta de {tokens[1]} no fue agregada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

    elif tokens[0] == 'del':
        variables = str(tokens[1])
        query = ("DELETE FROM Ventas WHERE id=%s")

        mensaje = 'dbges0:' + query + ':' + variables

        mensaje = generar_codigo(mensaje) + mensaje

        sock.send(mensaje.encode())

        while True:
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            data = data.decode()

            if data:
                print(data)
                data = data[7:]

                if data.split(":")[0] == '1':
                    print("Venta eliminada.")
                    newData = f'gvent Venta {tokens[1]} eliminada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Venta no eliminada.")
                    newData = f'gvent Venta no {tokens[1]} eliminada!'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
            else:
                print("Conexión cerrada por el servidor.")
                break

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

# Código principal

def main():
    ip = "127.0.0.1"  # Dirección IP del servidor local
    puerto = 5000  # Puerto del servidor local
    mensaje = "00010sinitgprod"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)

if __name__ == '__main__':
     
    main()

  
 

