import socket
import threading

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Aquí puedes procesar los datos recibidos y reenviarlos a los demás clientes
        print("Mensaje recibido:", data.decode())
        # Reenviar el mensaje a todos los clientes conectados
        for client in clients:
            if client != client_socket:
                client.send(data)

    client_socket.close()

# Configuración del servidor
host = 'localhost'
port = 6000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print(f"Servidor escuchando en {host}:{port}")

clients = []

while True:
    client_socket, addr = server_socket.accept()
    print("Cliente conectado:", addr)

    clients.append(client_socket)

    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
