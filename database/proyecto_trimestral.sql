-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-06-2021 a las 22:00:27
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
-- Estructura de tabla para la tabla `bank`
--

CREATE TABLE `bank` (
  `id` char(10) NOT NULL,
  `name` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cart_tmp`
--

CREATE TABLE `cart_tmp` (
  `id` int(11) NOT NULL,
  `product` int(4) UNSIGNED ZEROFILL DEFAULT NULL,
  `invoice` char(10) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `unit_value` float DEFAULT NULL,
  `total_iva` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cash_register`
--

CREATE TABLE `cash_register` (
  `number` tinyint(4) NOT NULL,
  `current_money` float DEFAULT 0,
  `base` float DEFAULT 0,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cash_register`
--

INSERT INTO `cash_register` (`number`, `current_money`, `base`, `date`) VALUES
(1, 5000, 5000, '2021-06-24 01:13:26'),
(2, 7500, 7500, '2021-06-24 19:47:20');

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
(4, 'Varios', 'Productos varios a disposición de nuestros clientes');

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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `invoices`
--

CREATE TABLE `invoices` (
  `uid` char(10) NOT NULL,
  `date` date NOT NULL,
  `seller` char(20) DEFAULT NULL,
  `customer` char(20) DEFAULT NULL,
  `total_value` float DEFAULT 0,
  `total_iva` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `invoices_details`
--

CREATE TABLE `invoices_details` (
  `uid` int(11) NOT NULL,
  `invoice` char(10) DEFAULT NULL,
  `product` int(4) UNSIGNED ZEROFILL DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `unit_value` float DEFAULT NULL,
  `total_iva` float DEFAULT NULL,
  `payment` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `payment_type`
--

CREATE TABLE `payment_type` (
  `code` int(11) NOT NULL,
  `pay` set('efectivo','tarjeta') NOT NULL DEFAULT 'efectivo',
  `bank` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `payment_type`
--

INSERT INTO `payment_type` (`code`, `pay`, `bank`) VALUES
(1, 'efectivo', NULL),
(2, 'tarjeta', NULL);

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
-- Indices de la tabla `bank`
--
ALTER TABLE `bank`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `cart_tmp`
--
ALTER TABLE `cart_tmp`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product` (`product`,`invoice`),
  ADD KEY `invoice` (`invoice`);

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
  ADD KEY `product` (`product`),
  ADD KEY `invoice` (`invoice`),
  ADD KEY `payment` (`payment`);

--
-- Indices de la tabla `payment_type`
--
ALTER TABLE `payment_type`
  ADD PRIMARY KEY (`code`),
  ADD KEY `bank` (`bank`);

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
-- AUTO_INCREMENT de la tabla `cart_tmp`
--
ALTER TABLE `cart_tmp`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `invoices_details`
--
ALTER TABLE `invoices_details`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cart_tmp`
--
ALTER TABLE `cart_tmp`
  ADD CONSTRAINT `cart_tmp_ibfk_1` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `cart_tmp_ibfk_2` FOREIGN KEY (`product`) REFERENCES `products` (`code`);

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
  ADD CONSTRAINT `invoices_details_ibfk_5` FOREIGN KEY (`product`) REFERENCES `products` (`code`),
  ADD CONSTRAINT `invoices_details_ibfk_6` FOREIGN KEY (`invoice`) REFERENCES `invoices` (`uid`),
  ADD CONSTRAINT `invoices_details_ibfk_7` FOREIGN KEY (`payment`) REFERENCES `payment_type` (`code`);

--
-- Filtros para la tabla `payment_type`
--
ALTER TABLE `payment_type`
  ADD CONSTRAINT `payment_type_ibfk_1` FOREIGN KEY (`bank`) REFERENCES `bank` (`id`);

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
