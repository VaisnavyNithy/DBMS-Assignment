-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 23, 2026 at 11:20 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbms_programming`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `User_id` char(5) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`User_id`, `Name`, `Email`) VALUES
('U001', 'Nimal Perera', 'nimalperera@gmail.com'),
('U002', 'Kavindi Silva', 'kavindisilva@yahoo.com'),
('U003', 'Ramesh Fernando', 'rameshfernando@hotmail.com'),
('U004', 'Hasini Jayawardena', 'hasinijaya@gmail.com'),
('U005', 'Tharindu Kumara', 'tharindukumara@gmail.com'),
('U006', 'Dilan Abeysekara', 'dilanabey@gmail.com'),
('U007', 'Isuri Nadeeshani', 'isuri34@gmail.com'),
('U008', 'Chamika Rathnayake', 'chamika87@gmail.com'),
('U009', 'Lakshan Perera', 'lakshan23@yahoo.com'),
('U010', 'Sanduni Fernando', 'sanduni12@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`User_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
