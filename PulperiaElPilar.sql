--CREAR LA BD 
CREATE DATABASE PulperiaElPilar

--USAR LA BD
USE PulperiaElPilar

/*----- CREACION DE TABLAS -----*/

--TABLAS INDEPENDIENTES
CREATE TABLE Producto
(
	codigo NVARCHAR(20) PRIMARY KEY NOT NULL,
	nombre NVARCHAR(30) NOT NULL,
	precio_unitario DECIMAL(10,2) DEFAULT 0,
	cantidad INT DEFAULT 0,
	categoria NVARCHAR(30),
	descripcion NVARCHAR(80)
)
GO

CREATE TABLE Cliente
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	nombres NVARCHAR(30) NOT NULL,
	apellidos NVARCHAR(30) NULL
)
GO

CREATE TABLE Proveedor
(
	id NVARCHAR(50) PRIMARY KEY NOT NULL,
	nombres NVARCHAR(30) NOT NULL,
	apellidos NVARCHAR(30) DEFAULT NULL,
	empresa NVARCHAR(50) NOT NULL,
	telefono CHAR(8) NOT NULL
)
GO

--TABLAS DEPENDIENTES

CREATE TABLE Compra
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	fecha DATE,
	total DECIMAL(10,2) DEFAULT 0,
	id_proveedor NVARCHAR(50),
	CONSTRAINT fk_proveedor_id FOREIGN KEY(id_proveedor) REFERENCES Proveedor(id)
)
GO

CREATE TABLE DetalleCompra
(
	codigo_detalle INT IDENTITY(1,1) PRIMARY KEY,
	cantidad INT NOT NULL,
	codigo_producto NVARCHAR(20),
	id_compra INT,
	CONSTRAINT fk_codigo_productoDC FOREIGN KEY(codigo_producto) REFERENCES Producto(codigo),
	CONSTRAINT fk_compra_id FOREIGN KEY(id_compra) REFERENCES Compra(id)
)
GO

CREATE TABLE Da�ado
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	descripcion NVARCHAR(80),
	fecha_registro DATE,
	total DECIMAL(10,2)
)
GO

CREATE TABLE DetalleDa�ado
(
	codigo_detalle INT IDENTITY(1,1) PRIMARY KEY,
	cantidad INT NOT NULL,
	estado_devolucion BIT DEFAULT 0,
	codigo_producto NVARCHAR(20),
	id_da�ado INT,
	CONSTRAINT fk_codigo_productoDD FOREIGN KEY(codigo_producto) REFERENCES Producto(codigo),
	CONSTRAINT fk_da�ado_id FOREIGN KEY(id_da�ado) REFERENCES Da�ado(id)
)
GO

--drop table DetalleDa�ado

CREATE TABLE Consumido
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	fecha_registro DATE,
	total DECIMAL(10,2)
)
GO

CREATE TABLE DetalleConsumido
(
	codigo_detalle INT IDENTITY(1,1) PRIMARY KEY,
	cantidad INT NOT NULL,
	codigo_producto NVARCHAR(20),
	id_consumido INT,
	CONSTRAINT fk_codigo_productoDCM FOREIGN KEY(codigo_producto) REFERENCES Producto(codigo),
	CONSTRAINT fk_consumido_id FOREIGN KEY(id_consumido) REFERENCES Consumido(id)
)
GO

CREATE TABLE Contado
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	fecha_registro DATE,
	total DECIMAL(10,2)
)
GO

CREATE TABLE DetalleContado
(
	codigo_detalle INT IDENTITY(1,1) PRIMARY KEY,
	cantidad INT NOT NULL,
	codigo_producto NVARCHAR(20),
	id_contado INT,
	CONSTRAINT fk_codigo_productoDCT FOREIGN KEY(codigo_producto) REFERENCES Producto(codigo),
	CONSTRAINT fk_contado_id FOREIGN KEY(id_contado) REFERENCES Contado(id)
)
GO

CREATE TABLE Credito
(
	id INT IDENTITY(1,1) PRIMARY KEY,
	fecha_credito DATE,
	fecha_cancelacion DATE,
	monto_pagado DECIMAL(10,2) DEFAULT 0,
	monto_pendiente DECIMAL(10,2),
	total DECIMAL(10,2),
	id_cliente INT,
	CONSTRAINT fk_cliente_id FOREIGN KEY(id_cliente) REFERENCES Cliente(id)
)
GO

CREATE TABLE DetalleCredito
(
	codigo_detalle INT IDENTITY(1,1) PRIMARY KEY,
	cantidad INT NOT NULL,
	codigo_producto NVARCHAR(20),
	id_credito INT,
	CONSTRAINT fk_codigo_productoDCD FOREIGN KEY(codigo_producto) REFERENCES Producto(codigo),
	CONSTRAINT fk_credito_id FOREIGN KEY(id_credito) REFERENCES Credito(id)
)
GO

/*----- FIN DE LAS TABLAS -----*/

/*Insertar datos NESTL�*/
INSERT INTO Producto (codigo, nombre,precio_unitario,cantidad,categoria,descripcion)
VALUES ('12552024', 'PRESTO CAFE STICK 60X(80X1.8G)', 167.83, 2, 'Bebida', 'Caf� presto instant�neo en presentaci�n de sticks'),
('12537279', 'MAGGI SOPA POLLO FIDEO 12X(12X55G)', 128.69, 2, 'Alimento', 'Sopa de fideo sabor pollo'),
('11296100', 'MAGGI SOPA CRI COSTILLA 12X(12X55G)', 125.65, 1, 'Alimentos', 'Sopa criolla sabor costilla'),
('12552068', 'NESCAFE CLASICO STICK 30X(20X1.8G)', 48.70, 1, 'Bebida', 'Caf� Nescafe cl�sico en sticks'),
('12585873', 'MAGGI CONSOME POLLO TIRA 40(14X10G)', 42.55, 2, 'Condimento', 'Sazonador de pollo en tiras'),
('12089991', 'MAGGI SAZ COSTILLA RES TIRA 40X(12X10G)', 37.03, 2, 'Condimento', 'Sazonador sabor costilla de res'),
('12588460', 'MAGGI SABORYCOLORCURCUMA40(12X10G)', 35.70, 2, 'Condimento', 'Sazonador sabor y color');

INSERT INTO Proveedor (id,nombres,apellidos,empresa,telefono)
VALUES('121','JUAN CARLOS','ARROLIGA VALDIVIA','NESTLE','83731941');

INSERT INTO Compra(fecha,total,id_proveedor)
VALUES('2024-12-10',1154.30,(SELECT id FROM Proveedor WHERE nombres = 'JUAN CARLOS'));

/*Insertar datos DELMOR*/
INSERT INTO Producto (codigo, nombre,precio_unitario,cantidad,categoria,descripcion)
VALUES ('04896372', 'RECORTE JAMON PRENSADO', 49.50, 3, 'Embutido', 'Embutido tipo Jamon Prensado'),
('078889642', 'MORTADELA POPULAR (227GR)', 33.90, 6, 'Embutido', 'Embutido tipo Mortadela presentacion 227 GR'),
('098633575', 'MORTADELA POPULAR (454GR)', 56.92, 2, 'Embutido', 'Embutido tipo Mortadela presentacion 454 GR'),
('049934212', 'CHORIZO CRIOLLO (227GR) REFRIGERADO', 34.35, 6, 'Embutido', 'Chorizo tipo criollo de 227 GR'),
('047792156', 'PUNTA DE LOMO DE CERDO IMPORTADO USA', 73.91, 38, 'Carnes', 'Punta de lomo de cerdo');

INSERT INTO Proveedor (id,nombres,apellidos,empresa,telefono)
VALUES('J0310000003718','HECTOR MARTIN','LANZAS ESPINOZA','DELMOR','87008073');

INSERT INTO Compra(fecha,total,id_proveedor)
VALUES('2024-10-23',809.10,(SELECT id FROM Proveedor WHERE nombres = 'HECTOR MARTIN')),
('2024-10-17',3229.87,(SELECT id FROM Proveedor WHERE nombres = 'HECTOR MARTIN'));


/*----- CONSULTAS Y EVALUACIONES (ddl,dml) -----*/
ALTER TABLE Producto
ALTER COLUMN nombre NVARCHAR(50)

EXEC sp_help 'Producto';

SELECT * FROM Cliente;

/*----- FIN DE LAS CONSULTAS -----*/