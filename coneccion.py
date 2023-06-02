import socket

def sum_numbers(num1, num2):
    return num1 + num2

def start_service():
    bus_host = "200.14.84.16"  # Dirección IP del bus
    bus_port = 5000

    # Crear un socket para el servicio local
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 5001))
    server_socket.listen(1)
    print("Servicio esperando conexiones en el puerto 5000")

    while True:
        client_socket, address = server_socket.accept()
        print("Conexión desde: " + str(address))

        # Establecer conexión con el bus remoto
        bus_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bus_socket.connect((bus_host, bus_port))
        print("Conexión establecida con el bus en la dirección: " + bus_host)

        # Enviar mensaje inicial al bus para activación
        init_message = "00010sinitsumar"
        bus_socket.send(init_message.encode())

        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Supongamos que las dos variables se envían separadas por una coma
            try:
                num1, num2 = map(int, data.split(','))
                sum_result = sum_numbers(num1, num2)
            except ValueError:
                sum_result = "Error: no se recibieron dos números"

            # Enviar los datos al bus remoto
            bus_socket.send(str(sum_result).encode())

            # Recibir la respuesta del bus
            response = bus_socket.recv(1024).decode()

            # Enviar la respuesta al cliente
            client_socket.send(response.encode())

        client_socket.close()

if __name__ == "__main__":
    start_service()
