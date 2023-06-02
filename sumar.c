#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#define MAX_BUFFER_SIZE 1024

void enviar_mensaje(const char* ip, int puerto, const char* mensaje) {
    int sockfd;
    struct sockaddr_in server_address;

    // Crear el socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("Error al crear el socket");
        exit(1);
    }

    // Configurar la dirección del servidor
    memset(&server_address, 0, sizeof(server_address));
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(puerto);
    if (inet_pton(AF_INET, ip, &(server_address.sin_addr)) <= 0) {
        perror("Error al configurar la dirección del servidor");
        exit(1);
    }

    // Conectar al servidor
    if (connect(sockfd, (struct sockaddr*)&server_address, sizeof(server_address)) < 0) {
        perror("Error al conectar al servidor");
        exit(1);
    }

    // Enviar el mensaje al servidor
    if (send(sockfd, mensaje, strlen(mensaje), 0) < 0) {
        perror("Error al enviar el mensaje");
        exit(1);
    }

    // Recibir y procesar las respuestas del servidor
    char buffer[MAX_BUFFER_SIZE];
    ssize_t num_bytes;
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        num_bytes = recv(sockfd, buffer, sizeof(buffer) - 1, 0);
        if (num_bytes > 0) {
            buffer[num_bytes] = '\0';
            printf("Respuesta recibida: %s\n", buffer);

            // Procesar la respuesta
            if (strlen(buffer) >= 10) {
                // Tamaño del mensaje
                char tamano_mensaje[6];
                strncpy(tamano_mensaje, buffer, 5);
                tamano_mensaje[5] = '\0';

                // Tipo de mensaje
                char tipo_mensaje[6];
                strncpy(tipo_mensaje, buffer + 5, 5);
                tipo_mensaje[5] = '\0';

                // Data
                char data[MAX_BUFFER_SIZE];
                strncpy(data, buffer + 10, sizeof(buffer) - 10);

                printf("Tamaño del mensaje: %s\n", tamano_mensaje);
                printf("Tipo de mensaje: %s\n", tipo_mensaje);
                printf("Data: %s\n", data);
    
                // Verificar si el mensaje es "sumar"
                char* token = strtok(data, " ");
                int var1, var2;
                int suma;

                if (token != NULL) {
                    var1 = atoi(token);
                    token = strtok(NULL, " ");
                }
                if (token != NULL) {
                    var2 = atoi(token);
                }

                // Realizar la suma
                suma = var1 + var2;

                // Construir la respuesta
                char respuesta[50];
                sprintf(respuesta, "00015sumar %d + %d = %d", var1, var2, suma);
                printf("mensaje enviado: %s\n", respuesta);

                // Enviar la respuesta al servidor
                if (send(sockfd, respuesta, strlen(respuesta), 0) < 0) {
                    perror("Error al enviar la respuesta");
                    exit(1);
                }
                // if (strcmp(tipo_mensaje, "sumar") == 0) {
                //     char respuesta[32];
                //     sprintf(respuesta, "00017sumarOK 2 + 3 = 5");
                //     printf("mensaje enviado: %s\n", respuesta);

                //     // Enviar la respuesta al servidor
                //     if (send(sockfd, respuesta, strlen(respuesta), 0) < 0) {
                //         perror("Error al enviar la respuesta");
                //         exit(1);
                //     }
                // }
            }
        } else if (num_bytes == 0) {
            printf("Conexión cerrada por el servidor.\n");
            break;
        } else {
            perror("Error al recibir la respuesta");
            break;
        }
    }

    // Cerrar la conexión
    close(sockfd);
}

int main() {
    const char* ip = "127.0.0.1"; // Dirección IP del servidor local
    int puerto = 5000; // Puerto del servidor local
    const char* mensaje = "00010sinitsumar"; // Mensaje a enviar

    enviar_mensaje(ip, puerto, mensaje);

    return 0;
}

           
