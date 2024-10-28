-- Crear tablas
CREATE DATABASE ARGBroker;
USE ARGBroker;

-- Crear tablas
CREATE TABLE inversores (
id INT AUTO_INCREMENT PRIMARY KEY,
cuit VARCHAR(20) UNIQUE NOT NULL,
nombre VARCHAR(50) NOT NULL,
apellido VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
contraseña VARCHAR(255) NOT NULL,
);

CREATE TABLE acciones (
id INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(10) UNIQUE NOT NULL,
nombre VARCHAR(100) NOT NULL,
precio_compra DECIMAL(10, 2),
precio_venta DECIMAL(10, 2),
cantidad_disponible INT
);

CREATE TABLE cotizaciones (
id INT AUTO_INCREMENT PRIMARY KEY,
accion_id INT,
fecha DATE,
precio DECIMAL(10, 2),
FOREIGN KEY (accion_id) REFERENCES acciones(id)
);

CREATE TABLE transacciones (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario_id INT,
accion_id INT,
tipo ENUM('compra', 'venta'),
cantidad INT,
precio DECIMAL(10, 2),
comision DECIMAL(10, 2),
fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
FOREIGN KEY (accion_id) REFERENCES acciones(id)
);

CREATE TABLE portafolio (
id INT AUTO_INCREMENT PRIMARY KEY,
usuario_id INT,
accion_id INT,
cantidad INT,
FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
FOREIGN KEY (accion_id) REFERENCES acciones(id)
);

-- Insertar datos en la tabla acciones
INSERT INTO acciones (codigo, nombre, precio_compra, precio_venta, cantidad_disponible) VALUES
('MCD', 'McDonald''s Corp', 316.56, 316.85, 2531197),
('KO', 'Coca-Cola Co', 70.57, 70.57, 2473903),
('GOOGL', 'Alphabet Inc', 233.85, 233.85, 2150000),
('AAPL', 'Apple Inc', 233.85, 233.85, 2150000),
('MSFT', 'Microsoft Corp', 418.74, 418.74, 2150000),
('TSLA', 'Tesla Inc', 219.57, 219.57, 2150000);

-- Actualizar el saldo de un usuario
UPDATE usuarios SET saldo = saldo + 1000 WHERE email = 'juan.perez@example.com';

-- Actualizar la contraseña de un usuario
UPDATE usuarios SET contraseña = 'nueva_contraseña' WHERE email = 'juan.perez@example.com';

-- Actualizar el precio de compra de una acción
UPDATE acciones SET precio_compra = 320.00 WHERE codigo = 'MCD';

-- Actualizar el precio de venta de una acción
UPDATE acciones SET precio_venta = 320.50 WHERE codigo = 'MCD';

-- Actualizar la cantidad disponible de una acción
UPDATE acciones SET cantidad_disponible = 2531000 WHERE codigo = 'MCD';

-- Obtener todos los inversores
SELECT * FROM inversores;

-- Obtener todas las transacciones de un inversor específico
SELECT * FROM transacciones WHERE cuit = '20304050607';

-- Obtener el saldo actual de un inversor
SELECT saldo FROM inversores WHERE cuit = '20304050607';

-- Obtener todas las acciones disponibles para la compra
SELECT * FROM acciones;

-- Obtener el historial de cotizaciones de una acción específica
SELECT * FROM cotizaciones WHERE codigo_accion = 'MCD'


###Obtener el historial de transacciones de un inversor junto con la información de las acciones**
SELECT t.id, t.cuit, a.nombre, t.tipo, t.cantidad, t.precio, t.total, t.fecha
FROM transacciones t
JOIN acciones a ON t.codigo_accion = a.codigo
WHERE t.cuit = '20304050607';

###Obtener la lista de inversores y sus activos actuales
SELECT i.cuit, i.nombre, i.apellido, a.codigo, a.nombre, a.precio_compra, a.precio_venta, t.cantidad
FROM inversores i
JOIN transacciones t ON i.cuit = t.cuit
JOIN acciones a ON t.codigo_accion = a.codigo
WHERE t.tipo = 'compra';


###Calcular el rendimiento total de un inversor
SELECT i.cuit, i.nombre, i.apellido, SUM((a.precio_venta - a.precio_compra) * t.cantidad) AS rendimiento_total
FROM inversores i
JOIN transacciones t ON i.cuit = t.cuit
JOIN acciones a ON t.codigo_accion = a.codigo
WHERE t.tipo = 'compra'
GROUP BY i.cuit;