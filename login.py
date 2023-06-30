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

    if tokens[0] == 'valida':
        # 00060gprodedit:11:manzana:editando la manzanita:2000:50:10/12/2023
        
        query = ("SELECT id, nombre, tienda_id FROM Usuarios WHERE nombre = %s and password=%s;")

        variables = tokens[1]

        mensaje = 'dbges1:' + query + ':' + variables

        print("Mensaje:", mensaje)
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

            print(data)
            
            if data:
                data = data[7:].split(':')
                if data[0] == '1':
                    print("Usario Encontrados.")
                    newData = f'logju1:{data[1]}'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Usuario no Encontrados.")
                    newData = f'logju Usuario no fue encontrado!'
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
    mensaje = "00010sinitlogju"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
