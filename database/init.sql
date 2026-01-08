CREATE DATABASE IF NOT EXISTS panificadora_la_merced_fn3;
USE panificadora_la_merced_fn3;

CREATE TABLE Cliente (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    telefono_celular VARCHAR(9)
);

CREATE TABLE Pago (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    metodo_pago BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Estado_Pedido (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    descripcion_estado VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE Pedido_cliente (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    tipo_entrega BOOLEAN NOT NULL DEFAULT FALSE,
    tipo_pedido BOOLEAN NOT NULL DEFAULT FALSE,
    cantidad_producto INT NOT NULL CHECK (cantidad_producto > 0),
    fecha DATE NOT NULL,
    id_cliente INT NOT NULL,
    id_pago INT NOT NULL,
    id_estado INT NOT NULL DEFAULT 1,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pago) REFERENCES Pago(id_pago) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_estado) REFERENCES Estado_Pedido(id_estado) ON UPDATE CASCADE
);

CREATE TABLE Detalle_Pedido (
    id_detalle_pedido INT PRIMARY KEY AUTO_INCREMENT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    id_pedido INT NOT NULL,
    FOREIGN KEY (id_pedido) REFERENCES Pedido_cliente(id_pedido) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (cantidad > 0),
    CHECK (precio_unitario >= 0)
);

CREATE TABLE Proveedor (
    id_proveedor INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    ruc VARCHAR(11) UNIQUE NOT NULL
);

CREATE TABLE Insumos (
    id_insumo INT PRIMARY KEY AUTO_INCREMENT,
    nombre_insumo VARCHAR(100) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,
    stock_minimo DECIMAL(10,3) NOT NULL CHECK (stock_minimo >= 0),
    stock_maximo DECIMAL(10,3) NOT NULL CHECK (stock_maximo >= 0)
);

CREATE TABLE Pedido_proveedor (
    id_abastecimiento INT PRIMARY KEY AUTO_INCREMENT,
    fecha_pedido DATE NOT NULL,
    fecha_entrega DATE,
    cantidad DECIMAL(10,3) NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    id_insumo INT NOT NULL,
    id_proveedor INT NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedor(id_proveedor) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_insumo) REFERENCES Insumos(id_insumo) ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (fecha_entrega IS NULL OR fecha_entrega >= fecha_pedido)
);

CREATE TABLE Producto (
    id_producto INT PRIMARY KEY AUTO_INCREMENT,
    nombre_producto VARCHAR(100) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    cantidad_producto INT DEFAULT 0 CHECK (cantidad_producto >= 0),
    id_insumos INT,
    id_pedido INT,
    FOREIGN KEY (id_insumos) REFERENCES Insumos(id_insumo) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pedido) REFERENCES Pedido_cliente(id_pedido) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Cargo (
    id_cargo INT PRIMARY KEY AUTO_INCREMENT,
    cargo VARCHAR(15) NOT NULL
);

CREATE TABLE Empleado (
    id_empleado INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    turno BOOLEAN NOT NULL DEFAULT FALSE,
    id_cargo INT NOT NULL,
    FOREIGN KEY (id_cargo) REFERENCES Cargo(id_cargo)
);

CREATE TABLE Produccion (
    id_produccion INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    turno boolean NOT NULL default false,
    cantidad_producida INT NOT NULL CHECK (cantidad_producida > 0),
    id_empleado INT NOT NULL,
    id_pedido INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pedido) REFERENCES Pedido_cliente(id_pedido) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==========================================
-- DATOS INICIALES (ORDEN CORRECTO)
-- ==========================================

-- 1. TABLAS SIN DEPENDENCIAS PRIMERO
INSERT INTO Estado_Pedido (descripcion_estado) VALUES 
    ('pendiente'),
    ('proceso'),
    ('completado'),
    ('cancelado');

INSERT INTO Cargo (cargo) VALUES 
    ('m_panad'),
    ('ayudante'),
    ('cont_pan');

INSERT INTO Pago (metodo_pago) VALUES
    (0), -- Efectivo
    (1); -- Yape

-- 2. CLIENTES
INSERT INTO Cliente (nombre, apellido_paterno, apellido_materno, telefono_celular) VALUES
('Juan', 'Pérez', 'Gómez', '987654321'),
('María', 'Lopez', 'Torres', '912345678'),
('Carlos', 'Rodríguez', 'Silva', '923456789'),
('Ana', 'Martínez', 'Vega', '934567890'),
('Luis', 'García', 'Flores', '945678901'),
('Rosa', 'Sánchez', 'Díaz', '956789012'),
('Pedro', 'Ramírez', 'Cruz', '967890123'),
('Julia', 'Torres', 'Mendoza', '978901234'),
('Miguel', 'Vargas', 'Rojas', '989012345'),
('Carmen', 'Castillo', 'Herrera', '990123456');

-- 3. PROVEEDORES
INSERT INTO Proveedor (nombre, apellido_paterno, apellido_materno, telefono, ruc) VALUES
('Roberto', 'Molina', 'Paz', '044-123456', '20123456789'),
('Gloria', 'Fernández', 'Luna', '044-234567', '20234567890'),
('Jorge', 'Quispe', 'Mamani', '044-345678', '20345678901'),
('Teresa', 'Huamán', 'Alvarez', '044-456789', '20456789012');

-- 4. INSUMOS
INSERT INTO Insumos (nombre_insumo, unidad_medida, stock_minimo, stock_maximo) VALUES
('Harina de Trigo', 'kg', 50.000, 500.000),
('Levadura', 'kg', 5.000, 50.000),
('Sal', 'kg', 10.000, 100.000),
('Azúcar', 'kg', 20.000, 200.000),
('Mantequilla', 'kg', 10.000, 100.000),
('Huevos', 'unidad', 100.000, 1000.000),
('Leche', 'litro', 20.000, 200.000),
('Chocolate', 'kg', 5.000, 50.000),
('Vainilla', 'litro', 2.000, 20.000),
('Canela', 'kg', 1.000, 10.000);

-- 5. EMPLEADOS (Ahora sí puede referenciar Cargo)
INSERT INTO Empleado (nombre, apellido_paterno, apellido_materno, turno, id_cargo) VALUES
('José', 'Paredes', 'Luján', 0, 1),      -- Panadero turno mañana
('Mario', 'Quispe', 'Flores', 1, 1),     -- Panadero turno tarde
('Sandra', 'Mejía', 'Castro', 0, 2),     -- Cajero turno mañana
('Patricia', 'Ramos', 'Vera', 1, 2),     -- Cajero turno tarde
('Ricardo', 'Chávez', 'Morales', 0, 3),  -- Repartidor turno mañana
('Fernando', 'Silva', 'Mendoza', 1, 3);  -- Repartidor turno tarde

-- 6. PRODUCTOS
INSERT INTO Producto (nombre_producto, precio_unitario, cantidad_producto) VALUES
('Pan Francés', 0.30, 100),
('Pan Integral', 0.50, 80),
('Torta Chocolate', 25.00, 5),
('Pan de Yema', 0.50, 60),
('Pan de Molde', 5.00, 20),
('Croissant', 2.50, 30),
('Empanada de Pollo', 3.50, 40),
('Empanada de Carne', 3.50, 35),
('Torta de Vainilla', 25.00, 3),
('Torta de Fresa', 28.00, 2),
('Alfajor', 1.50, 50),
('Suspiro Limeño', 4.00, 15),
('Queque Inglés', 1.00, 45),
('Rosquita', 0.80, 70),
('Pan de Camote', 0.60, 55);

-- 7. PEDIDOS A PROVEEDORES
INSERT INTO Pedido_proveedor (fecha_pedido, fecha_entrega, cantidad, precio_unitario, id_insumo, id_proveedor) VALUES
('2025-01-01', '2025-01-03', 100.000, 2.50, 1, 1),  -- Harina
('2025-01-01', '2025-01-03', 10.000, 15.00, 2, 1),  -- Levadura
('2025-01-02', '2025-01-04', 50.000, 1.20, 3, 2),   -- Sal
('2025-01-02', '2025-01-04', 80.000, 3.50, 4, 2),   -- Azúcar
('2025-01-03', '2025-01-05', 30.000, 12.00, 5, 3),  -- Mantequilla
('2025-01-03', '2025-01-05', 500.000, 0.50, 6, 3),  -- Huevos
('2025-01-04', '2025-01-06', 40.000, 4.00, 7, 4),   -- Leche
('2025-01-04', '2025-01-06', 15.000, 25.00, 8, 4),  -- Chocolate
('2025-01-05', NULL, 100.000, 2.50, 1, 1),          -- Pedido pendiente
('2025-01-06', NULL, 20.000, 12.00, 5, 3);          -- Pedido pendiente

-- 8. PEDIDOS DE CLIENTES
INSERT INTO Pedido_cliente (tipo_entrega, tipo_pedido, cantidad_producto, fecha, id_cliente, id_pago, id_estado) VALUES
-- Pedidos completados
(0, 0, 10, '2025-01-01', 1, 1, 3),  -- Recojo, Normal, Efectivo, Completado
(1, 0, 5, '2025-01-01', 2, 2, 3),   -- Delivery, Normal, Yape, Completado
(0, 1, 20, '2025-01-02', 3, 1, 3),  -- Recojo, Especial, Efectivo, Completado
(1, 0, 8, '2025-01-02', 4, 2, 3),   -- Delivery, Normal, Yape, Completado
(0, 0, 15, '2025-01-03', 5, 1, 3),  -- Recojo, Normal, Efectivo, Completado
-- Pedidos en proceso
(1, 1, 30, '2025-01-04', 6, 2, 2),  -- Delivery, Especial, Yape, En proceso
(0, 0, 12, '2025-01-05', 7, 1, 2),  -- Recojo, Normal, Efectivo, En proceso
(1, 0, 6, '2025-01-06', 8, 2, 2),   -- Delivery, Normal, Yape, En proceso
-- Pedidos pendientes
(0, 0, 25, '2025-01-07', 1, 1, 1),  -- Recojo, Normal, Efectivo, Pendiente
(1, 1, 40, '2025-01-07', 3, 2, 1),  -- Delivery, Especial, Yape, Pendiente
-- Pedido cancelado
(0, 0, 5, '2025-01-03', 2, 1, 4);   -- Recojo, Normal, Efectivo, Cancelado

-- 9. DETALLE DE PEDIDOS
-- Pedido 1 (Cliente Juan - 10 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(5, 0.30, 1),   -- 5 Pan Francés
(3, 0.50, 1),   -- 3 Pan Integral
(2, 2.50, 1);   -- 2 Croissant

-- Pedido 2 (Cliente María - 5 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(3, 3.50, 2),   -- 3 Empanada de Pollo
(2, 1.50, 2);   -- 2 Alfajor

-- Pedido 3 (Cliente Carlos - 20 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(10, 0.30, 3),  -- 10 Pan Francés
(5, 0.50, 3),   -- 5 Pan de Yema
(5, 1.00, 3);   -- 5 Queque Inglés

-- Pedido 4 (Cliente Ana - 8 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(1, 25.00, 4),  -- 1 Torta Chocolate
(4, 0.50, 4),   -- 4 Pan Integral
(3, 1.50, 4);   -- 3 Alfajor

-- Pedido 5 (Cliente Luis - 15 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(10, 0.30, 5),  -- 10 Pan Francés
(5, 0.80, 5);   -- 5 Rosquita

-- Pedido 6 (Cliente Rosa - 30 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(15, 0.30, 6),  -- 15 Pan Francés
(10, 0.50, 6),  -- 10 Pan de Yema
(5, 2.50, 6);   -- 5 Croissant

-- Pedido 7 (Cliente Pedro - 12 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(6, 3.50, 7),   -- 6 Empanada de Carne
(6, 1.00, 7);   -- 6 Queque Inglés

-- Pedido 8 (Cliente Julia - 6 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(1, 28.00, 8),  -- 1 Torta de Fresa
(5, 4.00, 8);   -- 5 Suspiro Limeño

-- Pedido 9 (Cliente Miguel - 25 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(20, 0.30, 9),  -- 20 Pan Francés
(5, 0.60, 9);   -- 5 Pan de Camote

-- Pedido 10 (Cliente Carmen - 40 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(20, 0.30, 10), -- 20 Pan Francés
(10, 0.50, 10), -- 10 Pan Integral
(10, 0.50, 10); -- 10 Pan de Yema

-- Pedido 11 cancelado (Cliente Carmen - 5 productos)
INSERT INTO Detalle_Pedido (cantidad, precio_unitario, id_pedido) VALUES
(5, 0.30, 11);  -- 5 Pan Francés

-- 10. REGISTROS DE PRODUCCIÓN
INSERT INTO Produccion (fecha, turno, cantidad_producida, id_empleado, id_pedido) VALUES
('2025-01-01', 0, 10, 1, 1),   -- José produjo pedido 1 en turno mañana
('2025-01-01', 1, 5, 2, 2),    -- Mario produjo pedido 2 en turno tarde
('2025-01-02', 0, 20, 1, 3),   -- José produjo pedido 3 en turno mañana
('2025-01-02', 1, 8, 2, 4),    -- Mario produjo pedido 4 en turno tarde
('2025-01-03', 0, 15, 1, 5),   -- José produjo pedido 5 en turno mañana
('2025-01-04', 0, 30, 1, 6),   -- José produjo pedido 6 en turno mañana
('2025-01-05', 1, 12, 2, 7),   -- Mario produjo pedido 7 en turno tarde
('2025-01-06', 0, 6, 1, 8);    -- José produjo pedido 8 en turno mañana