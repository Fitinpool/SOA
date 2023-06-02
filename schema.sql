SET @@global.time_zone = '-03:00';
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';

CREATE DATABASE IF NOT EXISTS gestion_tienda;
USE gestion_tienda;

CREATE TABLE Tiendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE Categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Categoria_Producto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    categoria_id INT,
    producto_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);

CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL,
    fecha_vencimiento DATE,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(id)
);

CREATE TABLE Ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL
);

CREATE TABLE Detalles_Ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES Ventas(id),
    FOREIGN KEY (producto_id) REFERENCES Productos(id)
);
