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
	metodo_pago BOOLEAN NOT NULL DEFAULT FALSE  -- falso= efectivo / verdadero=yape
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
    id_estado INT NOT NULL DEFAULT 1, -- Asume que 'pendiente' tiene el ID 1
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
    cargo VARCHAR(8) NOT NULL
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
    turno boolean NOT NULL default false,  -- mañana (0) tarde (1)
    cantidad_producida INT NOT NULL CHECK (cantidad_producida > 0),
    id_empleado INT NOT NULL,
    id_pedido INT NOT NULL,
    FOREIGN KEY (id_empleado) REFERENCES Empleado(id_empleado) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pedido) REFERENCES Pedido_cliente(id_pedido) ON DELETE CASCADE ON UPDATE CASCADE
);