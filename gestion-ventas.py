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

    if tokens[0] == 'addVenta':
        variables = str(datetime.strptime(tokens[1], '%d-%m-%Y').date())

        query = "INSERT INTO Ventas (fecha_venta) VALUES (%s)"

        mensaje = 'dbges1:' + query + ':' + variables

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
                    # Extraer el ID de la venta utilizando expresiones regulares
                    venta_id = re.search(r'Venta de \d+ agregada! ID: (\d+)', data)
                    if venta_id:
                        venta_id = venta_id.group(1)
                        print("ID de la venta:", venta_id)
                    else:
                        print("No se pudo obtener el ID de la venta.")
                        newData = f'gvent Venta de {tokens[1]} agregada!'
                        sock.send((generar_codigo(newData) + newData).encode())
                else:
                    print("Venta no agregada.")
                    newData = f'gvent Venta de {tokens[1]} no fue agregada!'
                    sock.send((generar_codigo(newData) + newData).encode())
            else :
                print("Conexión cerrada por el servidor.")
            break
    elif tokens[0] == 'addDet':
        venta_id = tokens[1]
        cant_prod = tokens[2]

        for i in range(cant_prod):
            tuplas = tokens[3 + i].split(",")
            producto_id = int(tuplas[0])
            cantidad = int(tuplas[1])
            precio = float(tuplas[2])

            query = "INSERT INTO Detalles_Ventas (venta_id, producto_id, cantidad, precio) VALUES (%s,%s,%s,%s)"
            variables = (venta_id, producto_id, cantidad, precio)

            mensaje = 'dbges1:' + query + ':' + ','.join(map(str, variables))

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
                        print("Detalle de venta agregado.")
                    else:
                        print("Detalle de venta no agregado.")
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
