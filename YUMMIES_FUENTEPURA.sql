USE PulperiaElPilar;

-- Insertar productos
INSERT INTO Producto (codigo, nombre, precio_unitario, cantidad, categoria, descripcion)
VALUES
    ('P001', 'Zibas Papa', 10.00, 24, 'Botanas', 'Queso'),
    ('P002', 'Zibas Papa', 10.00, 36, 'Botanas', 'Crema y especias'),
    ('P003', 'Zibas Papa', 10.00, 36, 'Botanas', 'Clasicas'),
    ('P004', 'Zibas Papa', 10.00, 24, 'Botanas', 'Miel Mostaza'),
    ('P005', 'Chicharron Picositos', 10.00, 36, 'Botanas', '-'),
    ('P006', 'Ranchita', 27.00, 10, 'Botanas', 'Queso 70g'),
    ('P007', 'Taqueritos', 15.00, 48, 'Botanas', 'QuesoFusion'),
    ('P008', 'Yummipop', 10.00, 24, 'Botanas', 'SalMar'),
    ('P009', 'Taco Tornitos', 4.00, 12, 'Botanas', 'Chile Toreado'),
    ('P010', 'Ranchita', 11.00, 60, 'Botanas', 'Nacho queso'),
    ('P011', 'Ranchita', 11.00, 12, 'Botanas', 'Nacho pizza'),
    ('P012', 'Taqueritos', 15.00, 24, 'Botanas', 'Dragon Hielo'),
    ('P013', 'Taqueritos', 27.00, 4, 'Botanas', 'Dragon hielo 80g'),
    ('P014', 'Cappy Infladitos', 8.00, 24, 'Botanas', 'Queso'),
    ('P015', 'Anillitos', 7.00, 48, 'Botanas', 'Papa Jalapeño'),
    ('P016', 'Taqueritos', 27.00, 3, 'Botanas', 'ChileTor 80g'),
    ('P017', 'Zambo Yuquita', 5.00, 12, 'Botanas', 'ChileTor'),
    ('P018', 'Taqueritos', 15.00, 36, 'Botanas', 'ChileTor'),
    ('P019', 'Cappy Infladitos', 25.00, 3, 'Botanas', 'Queso 70g'),
    ('P020', 'Anillitos', 7.00, 36, 'Botanas', 'Papa Barbacoa'),
    ('P021', 'Taqueritos', 15.00, 60, 'Botanas', 'ChileTor'),
    ('P022', 'Yumix', 14.00, 12, 'Botanas', 'Tropical'),
    ('P023', 'Yummipop', 10.00, 12, 'Botanas', 'Queso'),
    ('P024', 'Zambos', 8.00, 12, 'Botanas', 'Ceviche'),
    ('P025', 'Ranchita', 11.00, 36, 'Botanas', 'Queso Excitante'),
    ('P026', 'Ranchita', 11.00, 12, 'Botanas', 'Guacamole'),
    ('0080', 'Agua', 19.00, 12, 'Bebida', 'Fuente Pura 600'),
    ('1542', 'Agua', 15.00, 36, 'Bebida', 'Brisa 500ml'),
    ('1456', 'Agua', 22.00, 6, 'Bebida', 'Fp 1L'),
    ('83', 'Agua', 22.00, 6, 'Bebida', 'Fp 1.5L'),
    ('75', 'Agua', 40.00, 4, 'Bebida', 'Galon'),
    ('2166', 'Dfrutta', 10.00, 24, 'Bebida', 'Mandarina'),
    ('2170', 'Dfrutta', 10.00, 36, 'Bebida', 'Manzana'),
    ('2174', 'Dfrutta', 10.00, 36, 'Bebida', 'Sandia'),
    ('1721', 'Dfrutta', 48.00, 8, 'Bebida', 'Sandia 3L'),
    ('1717', 'Dfrutta', 48.00, 4, 'Bebida', 'Naranja 3L'),
    ('010205007', 'Milko', 34.00, 48, 'Bebida', 'Fortificada'),
    ('5158', 'Naturas Salsa', 14.00, 96, 'Aderezo', 'Tomate'),
    ('1950', 'Nutri Lety', 42.00, 48, 'Bebida', '1L'),
    ('3263', 'Torti Chips', 5.00, 60, 'Botana', 'Limon'),
    ('1823', 'Dfrutta', 44.00, 18, 'Bebida', 'Doypack rosca');

-- Insertar compras
INSERT INTO Compra (fecha, total, id_proveedor)
VALUES
    ('2024-10-15', 1570.07, '0016006237'),
    ('2024-10-23', 1613.02, '0016006237'),
    ('2024-10-29', 1751.50, '0016006237'),
    ('2024-10-23', 1730.28, '5661706820000Y'),
    ('2024-10-09', 607.86, '5661706820000Y'),
    ('2024-10-01', 1261.76, '5661706820000Y');

-- Insertar proveedores
INSERT INTO Proveedor (id, nombres, apellidos, empresa, telefono)
VALUES
    ('0016006237', 'Mauricio Manuel', 'Narvaez', 'Yummies', '-'),
    ('5661706820000Y', 'Elvis', 'Martinez', 'DIPROVIRSA', '22325812');

-- Insertar detalles de compra
INSERT INTO DetalleCompra (codigo_detalle, cantidad, codigo_producto, id_compra)
VALUES
    (1, 12, '12021', 1),
    (1, 12, '12022', 1),
    (1, 24, '12023', 1),
    (1, 24, '12024', 1),
    (1, 12, '12025', 1),
    (1, 12, '12026', 1),
    (1, 24, '12027', 1),
    (1, 12, '12028', 1),
    (1, 24, '12029', 1),
    (1, 12, '12030', 1),
    (1, 12, '12031', 1),
    (1, 24, '12032', 1),
    (2, 12, '12036', 2),
    (2, 24, '12037', 2),
    (2, 12, '12038', 2),
    (2, 24, '12039', 2),
    (2, 12, '12040', 2),
    (2, 6, '12041', 2),
    (2, 3, '12042', 2),
    (3, 12, '12051', 3),
    (3, 12, '12052', 3),
    (3, 24, '12053', 3),
    (4, 12, '0080', 4),
    (4, 18, '1542', 4),
    (4, 6, '1456', 4),
    (4, 6, '83', 4),
    (4, 4, '75', 4),
    (5, 18, '1542', 5),
    (5, 48, '3263', 5),
    (5, 12, '2166', 5),
    (6, 18, '1823', 6),
    (6, 12, '2170', 6),
    (6, 12, '2174', 6);

-- Consultar productos ordenados por precio unitario
SELECT * FROM Producto
ORDER BY precio_unitario ASC;

-- Consultar detalles de compra ordenados por cantidad
SELECT * FROM DetalleCompra
ORDER BY cantidad ASC;
