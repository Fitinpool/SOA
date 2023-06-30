#!/bin/bash

# Función para manejar la terminación del script
cleanup() {
    echo "Cerrando los servicios de Docker Compose..."
    docker-compose down

    # Terminar el script Python
    kill -- -$$
}

trap 'cleanup' SIGINT SIGTERM

# Ejecutar docker-compose
docker-compose up -d

# Esperar para asegurarnos de que los servicios de Docker Compose hayan comenzado
sleep 60

# Ejecutar el archivo Python
python3 ./tunel-ssh.py
