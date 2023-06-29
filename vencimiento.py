import socket
from datetime import datetime, timedelta

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

    if tokens[0] == 'list':
        fecha_actual = datetime.now().date()
        fecha_actual = fecha_actual.strftime('%d/%m/%Y')
        fecha_comparar = fecha_actual - timedelta(days=10)

        query = ("SELECT id, nombre, descripcion, precio, stock, fecha_vencimiento FROM Productos WHERE fecha_vencimiento BETWEEN %s AND %s ORDER BY fecha_vencimiento ASC")
        
        mensaje = 'dbges1:' + query + ':' + fecha_comparar + ',' + fecha_actual

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
                    newData = f'stock{data[1]}'
                    sock.send((generar_codigo(newData) + newData).encode())
                    break
                else:
                    print("Producto no Encontrados.")
                    newData = f'stock No existen productos cerca a vencer (10 días)'
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
    mensaje = "00010sinitvence"  # Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje)


if __name__ == "__main__":
    main()
