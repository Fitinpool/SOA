import wexpect
import time
from dotenv import load_dotenv
import os

load_dotenv()

def execute_ssh_command(user, ip, port, local_port, remote_port, password):
    command = f"ssh -L {local_port}:localhost:{remote_port} {user}@{ip} -p {port}"

    print(command)

    while True:
        try:
            child = wexpect.spawn(command)
            
            # El comando SSH pide una contraseña
            child.expect('password:')
            child.sendline(password)
            
            # Asegurarse de que el proceso ssh está en ejecución, de lo contrario,
            # lanzará una excepción y se volverá a intentar
            print("Conexión establecida. Presione Ctrl + C para cerrarla.")
            child.expect(wexpect.EOF, timeout=None)

        except (wexpect.EOF, wexpect.TIMEOUT):
            print("Conexión interrumpida. Reintentando en 5 segundos...")
            time.sleep(5)
            continue
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            break

execute_ssh_command(os.getenv('USER_DOCENCIA'), os.getenv('IP'), 8080, 5000, 5000, os.getenv('PASSWORD_DOCENCIA'))
