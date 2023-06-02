import socket

MAX_BUFFER_SIZE = 1024

def enviar_mensaje(ip, puerto, mensaje):
    # Crear el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conectar al servidor
        sock.connect((ip, puerto))

        # Enviar el mensaje al servidor
        sock.send(mensaje.encode())

        while True:
            # Recibir y mostrar la respuesta del servidor
            data = sock.recv(MAX_BUFFER_SIZE).decode()
            if data:
                print("Respuesta recibida:", data)
                break
            else:
                # Si no hay datos, el servidor ha cerrado la conexión
                break
    except socket.error as e:
        print("Error de socket:", e)
    finally:
        # Cerrar la conexión
        sock.close()

def main():
    ip = "127.0.0.1"  # Dirección IP del servidor
    puerto = 5000  # Puerto del servidor

    while True:
        # Esperar entrada por teclado
        mensaje = input("Ingrese un mensaje (o 'salir' para terminar): ")

        # Verificar si se desea salir
        if mensaje == 'salir':
            break

        # Enviar el mensaje al servidor
        enviar_mensaje(ip, puerto, mensaje)

if __name__ == "__main__":
    main()
