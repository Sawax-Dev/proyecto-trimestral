-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-06-2021 a las 10:43:14
-- Versión del servidor: 10.4.19-MariaDB
-- Versión de PHP: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto_trimestral`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cash_register`
--

CREATE TABLE `cash_register` (
  `number` tinyint(4) NOT NULL,
  `base` float DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cash_register`
--

INSERT INTO `cash_register` (`number`, `base`, `date`) VALUES
(1, 5000, '2021-06-24 01:13:26'),
(2, 7500, '2021-06-24 19:47:20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `category`
--

CREATE TABLE `category` (
  `code` tinyint(11) NOT NULL,
  `name` char(40) NOT NULL,
  `description` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `category`
--

INSERT INTO `category` (`code`, `name`, `description`) VALUES
(1, 'Alimentos', 'Todos los productos alimenticios'),
(2, 'Bebidas', 'Todos los productos líquidos disponibles'),
(3, 'Aseo', 'Solo productos de aseo y limpieza'),
(4, 'Varios', 'Productos varios a disposición de nuestros clientes'),
(5, 'Test', 'Any');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `customers`
--

CREATE TABLE `customers` (
  `id` char(20) NOT NULL,
  `name` char(50) DEFAULT NULL,
  `last_name` char(60) DEFAULT NULL,
  `id_type` set('CC','TI') DEFAULT NULL,
  `phone` char(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `customers`
--

INSERT INTO `customers` (`id`, `name`, `last_name`, `id_type`, `phone`) VALUES
('78999321', 'Test', 'Testing', 'CC', '3113003030');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `invoices`
--

CREATE TABLE `invoices` (
  `uid` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `seller` char(20) DEFAULT NULL,
  `customer` char(20) DEFAULT NULL,
  `total_value` float DEFAULT NULL,
  `total_iva` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `invoices_details`
--

CREATE TABLE `invoices_details` (
  `uid` int(11) NOT NULL,
  `invoice` int(11) DEFAULT NULL,
  `product` int(4) UNSIGNED ZEROFILL DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `total_iva` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `invoices_details`
--

INSERT INTO `invoices_details` (`uid`, `invoice`, `product`, `quantity`, `unit_value`, `total_iva`) VALUES
(1, NULL, 0001, 2, 13500, 0),
(2, NULL, 0002, 1, 900, 0),
(3, NULL, 0004, 5, 4444, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `code` int(4) UNSIGNED ZEROFILL NOT NULL,
  `name` char(40) NOT NULL,
  `stock` int(11) NOT NULL DEFAULT 0,
  `value` float NOT NULL,
  `iva` decimal(10,0) DEFAULT 0,
  `discount` float DEFAULT 0,
  `category` tinyint(4) DEFAULT NULL,
  `expiration_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`code`, `name`, `stock`, `value`, `iva`, `discount`, `category`, `expiration_date`) VALUES
(0001, 'Arroz', 180, 13500, '0', 0, 1, '2024-12-31'),
(0002, 'Papa', 500, 900, '0', 0, 1, '2021-06-30'),
(0003, 'Garbanzo', 4000, 40, '0', 0, 1, '2023-11-22'),
(0004, 'Test', 1234, 4444, '0', 0, 3, '2021-06-23'),
(0005, 'Papaya', 10, 3500, '0', 0, 1, '2021-07-10'),
(0006, 'Guanabana', 20, 2700, '0', 0, 1, '2021-06-24'),
(0007, 'Chocolate', 16, 250, '0', 0, 2, '2021-06-30'),
(0046, 'Test', 0, 5600, '0', 0, 1, '2021-06-28'),
(0098, 'Test', 56, 10050, '0', 0, 1, '2021-06-22'),
(0099, 'Almendras', 78, 6700, '0', 0, 1, '2021-07-07'),
(0100, 'asdasd', 123, 2222, '0', 0, 4, '2021-06-29'),
(0101, 'Loli', 15, 22222, '0', 0, 1, '2021-06-29'),
(0567, 'Test', 13, 5600, '0', 0, 1, '2021-06-29'),
(1123, 'Huevos', 5, 3444, '0', 0, 1, '2021-07-05'),
(9998, 'Sardinas', 150, 6700, '0', 0, 1, '2021-06-30'),
(9999, 'test', 9999, 999999, '99999', 0, 5, '2021-06-04');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `identity` char(20) NOT NULL,
  `id_type` set('CC','TI') NOT NULL,
  `name` char(50) NOT NULL,
  `last_name` char(60) NOT NULL,
  `email` varchar(80) NOT NULL,
  `password` varchar(350) NOT NULL,
  `role` set('Usuario','Administrador') DEFAULT 'Usuario',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `register_number` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`identity`, `id_type`, `name`, `last_name`, `email`, `password`, `role`, `created_at`, `register_number`) VALUES
('1098306124', 'TI', 'Brian', 'Castro Bedoya', 'bcastro421@misena.edu.co', 'pbkdf2:sha256:260000$VhSPsUazELCnqAca$1ecf9962fc1a3208a987b4364f420005c5f4cf23dd83d2747649525ae05c9826', 'Usuario', '2021-06-23 00:49:36', 1),
('41945032', 'CC', 'Yito', 'Caballito', 'test@mail.com', 'pbkdf2:sha256:260000$nFhDPk1UvrfXM7U2$1a939f3f78690fb09625209d6941aef39814764674136d754fdc6bedccc145ba', 'Administrador', '2021-06-23 00:49:36', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cash_register`
--
ALTER TABLE `cash_register`
  ADD PRIMARY KEY (`number`);

--
-- Indices de la tabla `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`code`);

--
-- Indices de la tabla `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`uid`),
  ADD KEY `customer` (`customer`),
  ADD KEY `seller` (`seller`);

--
-- Indices de la tabla `invoices_details`
--
ALTER TABLE `invoices_details`
  ADD PRIMARY KEY (`uid`),
  ADD KEY `invoice` (`invoice`),
  ADD KEY `product` (`product`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`code`),
  ADD KEY `category` (`category`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`identity`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `register_number` (`register_number`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `invoices`
--
ALTER TABLE `invoices`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `invoices_details`
--
ALTER TABLE `invoices_details`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `invoices`
--
ALTER TABLE `invoices`
  ADD CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`customer`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `invoices_ibfk_2` FOREIGN KEY (`customer`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `invoices_ibfk_3` FOREIGN KEY (`customer`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `invoices_ibfk_4` FOREIGN KEY (`customer`) REFERENCES `customers` (`id`),
  ADD CONSTRAINT `invoices_ibfk_5` FOREIGN KEY (`seller`) REFERENCES `users` (`identity`);

--
-- Filtros para la tabla `invoices_details`
--
ALTER TABLE `invoices_details`
  ADD CONSTRAINT `invoices_details_ibfk_1` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `invoices_details_ibfk_2` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `invoices_details_ibfk_3` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `invoices_details_ibfk_4` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `invoices_details_ibfk_5` FOREIGN KEY (`product`) REFERENCES `products` (`code`);

--
-- Filtros para la tabla `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category`) REFERENCES `category` (`code`);

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`register_number`) REFERENCES `cash_register` (`number`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
