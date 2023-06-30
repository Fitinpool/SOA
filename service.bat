@echo off

REM Función para manejar la terminación del script
:cleanup
echo Cerrando los servicios de Docker Compose...
docker-compose down


REM Ejecutar docker-compose
docker-compose up -d

REM Esperar para asegurarnos de que los servicios de Docker Compose hayan comenzado
ping 127.0.0.1 -n 61 > nul

REM Ejecutar el archivo Python
python tunel-ssh.py
