CREATE DATABASE IF NOT EXISTS ARGBroker;

USE ARGBroker;

-- CREATE TABLE Inversores (
--     cuit VARCHAR(11) PRIMARY KEY,
--     nombre VARCHAR(100),
--     apellido VARCHAR(100),
--     email VARCHAR(100) UNIQUE,
--     contraseña VARCHAR(255),
--     saldo DECIMAL(15, 2)
-- );

-- CREATE TABLE Acciones (
--     codigo VARCHAR(10) PRIMARY KEY,
--     nombre VARCHAR(100),
--     precio_compra DECIMAL(10, 2),
--     precio_venta DECIMAL(10, 2),
--     cantidad_disponible INT
-- );

-- CREATE TABLE Transacciones (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     cuit VARCHAR(11),
--     codigo_accion VARCHAR(10),
--     tipo ENUM('compra', 'venta'),
--     cantidad INT,
--     precio DECIMAL(10, 2),
--     total DECIMAL(15, 2),
--     fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (cuit) REFERENCES Inversores(cuit),
--     FOREIGN KEY (codigo_accion) REFERENCES Acciones(codigo)
-- );

-- CREATE TABLE Cotizaciones (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     codigo_accion VARCHAR(10),
--     precio DECIMAL(10, 2),
--     fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (codigo_accion) REFERENCES Acciones(codigo)
-- );

-- INSERT INTO Acciones (codigo, nombre, precio_compra, precio_venta, cantidad_disponible) VALUES
-- ('MCD', 'McDonald''s', 200.00, 210.00, 1000),
-- ('AAPL', 'Apple', 300.00, 320.00, 500),
-- ('GOOGL', 'Google', 1500.00, 1550.00, 300),
-- ('KO', 'Coca-Cola Co.', 56.80, 57.20, 1000),
-- ('SAMS', 'Samsung Electronics', 78.50, 79.00, 1000),
-- ('NFLX', 'Netflix Inc.', 590.70, 595.00, 1000),
-- ('DIS', 'The Walt Disney Co.', 180.25, 181.00, 1000),
-- ('NKE', 'Nike Inc.', 156.50, 157.20, 1000);

-- Insertar algunos inversores
-- INSERT INTO Inversores (cuit, nombre, apellido, email, contraseña, saldo) VALUES
-- ('20304050607', 'Juan', 'Perez', 'juan.perez@gmail.com', 'hashed_password', 1000000.00),
-- ('30102030405', 'Maria', 'Lopez', 'maria.lopez@gmail.com', 'hashed_password', 1000000.00);

-- Insertar algunas cotizaciones
-- INSERT INTO Cotizaciones (codigo_accion, precio) VALUES
-- ('MCD', 210.00),
-- ('AAPL', 320.00),
-- ('GOOGL', 1550.00);

-- Insertar algunas transacciones
-- INSERT INTO Transacciones (cuit, codigo_accion, tipo, cantidad, precio, total) VALUES
-- ('20304050607', 'MCD', 'compra', 10, 200.00, 2000.00),
-- ('30102030405', 'AAPL', 'compra', 5, 300.00, 1500.00);

-- Actualizar el saldo de un inversor
-- UPDATE Inversores SET saldo = saldo + 5000 WHERE cuit = '20304050607';

-- Actualizar el precio de compra de una acción
-- UPDATE Acciones SET precio_compra = 220.00 WHERE codigo = 'MCD';

-- Actualizar el precio de venta de una acción
-- UPDATE Acciones SET precio_venta = 330.00 WHERE codigo = 'AAPL';

-- Actualizar la cantidad disponible de una acción
-- UPDATE Acciones SET cantidad_disponible = 1500 WHERE codigo = 'GOOGL';

-- Actualizar el estado de bloqueo de un inversor
-- UPDATE Inversores SET bloqueado = TRUE WHERE cuit = '30102030405';

-- Obtener todos los inversores
-- SELECT * FROM inversores;

-- Obtener todas las transacciones de un inversor específico
-- SELECT * FROM transacciones WHERE cuit = '20304050607';

-- Obtener el saldo actual de un inversor
-- SELECT saldo FROM inversores WHERE cuit = '20304050607';

-- Obtener todas las acciones disponibles para la compra
-- SELECT * FROM acciones;

-- Obtener el historial de cotizaciones de una acción específica
-- SELECT * FROM cotizaciones WHERE codigo_accion = 'MCD';

-- Obtener el historial de transacciones de un inversor junto con la información de las acciones
-- SELECT t.id, t.cuit, a.nombre, t.tipo, t.cantidad, t.precio, t.total, t.fecha
-- FROM transacciones t
-- JOIN acciones a ON t.codigo_accion = a.codigo
-- WHERE t.cuit = '20304050607';

-- Obtener la lista de inversores y sus activos actuales
-- SELECT i.cuit, i.nombre, i.apellido, a.codigo, a.nombre, a.precio_compra, a.precio_venta, t.cantidad
-- FROM inversores i
-- JOIN transacciones t ON i.cuit = t.cuit
-- JOIN acciones a ON t.codigo_accion = a.codigo
-- WHERE t.tipo = 'compra';

-- Calcular el rendimiento total de un inversor
-- SELECT i.cuit, i.nombre, i.apellido, SUM((a.precio_venta - a.precio_compra) * t.cantidad) AS rendimiento_total
-- FROM inversores i
-- JOIN transacciones t ON i.cuit = t.cuit
-- JOIN acciones a ON t.codigo_accion = a.codigo
-- WHERE t.tipo = 'compra'
-- GROUP BY i.cuit;

SELECT * FROM acciones;
