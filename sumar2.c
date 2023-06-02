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

    // Recibir y mostrar la respuesta del servidor
    char buffer[MAX_BUFFER_SIZE];
    ssize_t num_bytes;
    while ((num_bytes = recv(sockfd, buffer, sizeof(buffer) - 1, 0)) > 0) {
        buffer[num_bytes] = '\0';
        printf("Respuesta recibida: %s\n", buffer);
        memset(buffer, 0, sizeof(buffer));
    }

    // Cerrar la conexión
    close(sockfd);
}

int main() {
    const char* ip = "127.0.0.1"; // Dirección IP del servidor
    int puerto = 5000; // Puerto del servidor

    char mensaje[MAX_BUFFER_SIZE];

    while (1) {
        // Esperar entrada por teclado
        printf("Ingrese un mensaje (o 'salir' para terminar): ");
        fgets(mensaje, sizeof(mensaje), stdin);

        // Eliminar el carácter de nueva línea
        mensaje[strcspn(mensaje, "\n")] = '\0';

        // Verificar si se desea salir
        if (strcmp(mensaje, "salir") == 0) {
            break;
        }

        // Separar la data por espacios
        char* token = strtok(mensaje, " ");
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
        sprintf(respuesta, "%d + %d = %d", var1, var2, suma);
        printf("Respuesta: %s\n", respuesta);

        // Enviar la respuesta al servidor
        enviar_mensaje(ip, puerto, respuesta);
    }

    return 0;
}
