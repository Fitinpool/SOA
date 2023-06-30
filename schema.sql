SET @@global.time_zone = '-03:00';
SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';

CREATE DATABASE IF NOT EXISTS gestion_tienda;
USE gestion_tienda;

-- Table: Tiendas
CREATE TABLE `Tiendas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Productos
CREATE TABLE `Productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `descripcion` text,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `fecha_vencimiento` date DEFAULT NULL,
  `tienda_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `Productos_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `Tiendas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Categorias
CREATE TABLE `Categorias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `tienda_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `Categorias_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `Tiendas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Categoria_Producto
CREATE TABLE `Categoria_Producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `categoria_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `categoria_id` (`categoria_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `Categoria_Producto_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `Categorias` (`id`),
  CONSTRAINT `Categoria_Producto_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Usuarios
CREATE TABLE `Usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `tienda_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `Usuarios_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `Tiendas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Ventas
CREATE TABLE `Ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_venta` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `tienda_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tienda_id` (`tienda_id`),
  CONSTRAINT `Ventas_ibfk_1` FOREIGN KEY (`tienda_id`) REFERENCES `Tiendas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Detalles_Ventas
CREATE TABLE `Detalles_Ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `venta_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `Detalles_Ventas_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `Ventas` (`id`),
  CONSTRAINT `Detalles_Ventas_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `Productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table: Historial_Precios
CREATE TABLE `Historial_Precios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `precio` decimal(10,2) NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `Historial_Precios_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `Productos` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

