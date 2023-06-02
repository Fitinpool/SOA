import socket
import struct

MAX_BUFFER_SIZE = 1024

def procesar_mensaje(data_mensaje, sock):
    # Removiendo espacios al inicio y al final
    data_mensaje = data_mensaje.strip()

    # Tamaño del mensaje
    tamano_mensaje = int(data_mensaje[:5])

    # Tipo de mensaje
    tipo_mensaje = data_mensaje[5:10].strip()

    # Data
    data = data_mensaje[10:]

    print("Tamaño del mensaje:", tamano_mensaje)
    print("Tipo de mensaje:", tipo_mensaje)
    print("Data:", data)

    # Procesar la data
    tokens = data.split(" ")

    # Comprobar que hay al menos dos tokens para realizar la operación
    # Procesar la data
    tokens = data.strip().split(" ")

    # Comprobar que hay al menos dos tokens para realizar la operación
    if len(tokens) >= 2:
        num1 = int(tokens[0]) if tokens[0] != '' else 0
        num2 = int(tokens[1]) if tokens[1] != '' else 0

        resultado = num1 + num2

        print("Resultado:", resultado)
        newData = 'sumar ' + str(num1) + ' + ' + str(num2) + ' = ' + str(resultado)
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
        data = sock.recv(MAX_BUFFER_SIZE).decode()
        
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
    mensaje = "00010sinitsumar"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
