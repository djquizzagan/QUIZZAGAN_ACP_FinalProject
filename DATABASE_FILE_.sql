-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 12, 2024 at 01:21 AM
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
-- Database: `roomradardb`
--

-- --------------------------------------------------------

--
-- Table structure for table `guest`
--

CREATE TABLE `guest` (
  `GuestID` int(11) NOT NULL,
  `GuestName` varchar(100) NOT NULL,
  `CellphoneNumber` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guest`
--

INSERT INTO `guest` (`GuestID`, `GuestName`, `CellphoneNumber`) VALUES
(18, 'Juan Castromerio', '09685743215'),
(19, 'Freddie Arinzaso', '09718345732'),
(20, 'Leslie Perea', '09128904501'),
(21, 'Julio Dagupan', '09394789324'),
(22, 'Gladilyn Trinidad', '09164508602'),
(23, 'Daniel Fenaranda', '09563248722'),
(24, 'Tessie Villapando', '09461238580'),
(25, 'Louie Paz', '09186628133'),
(26, 'Maria Magadia', '09194765431'),
(27, 'Lucine Delacruz', '09124504432'),
(28, 'Melchor Serrano', '09859923221'),
(29, 'David Salazar', '09602315666'),
(30, 'Hilario De Mesa', '09604389041'),
(34, 'Delia Garote', '09374832842'),
(35, 'Marcy Arevalo', '09462340198'),
(36, 'shaine ', '123456789876543'),
(37, 'Deniel', '09462368123'),
(38, 'Deniel John ', '09461368285'),
(39, 'Deniel John', '09461368285');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `ReservationID` int(11) NOT NULL,
  `GuestID` int(11) NOT NULL,
  `RoomID` int(11) NOT NULL,
  `ReservationDate` date NOT NULL,
  `NumberOfDays` int(11) NOT NULL,
  `TotalPrice` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`ReservationID`, `GuestID`, `RoomID`, `ReservationDate`, `NumberOfDays`, `TotalPrice`) VALUES
(11, 18, 101, '2024-12-05', 2, 1800.00),
(12, 19, 105, '2025-01-23', 5, 12500.00),
(13, 20, 107, '2024-12-30', 1, 3300.00),
(14, 21, 108, '2025-01-20', 2, 7400.00),
(15, 22, 102, '2024-11-29', 5, 6500.00),
(16, 23, 107, '2025-02-02', 2, 6600.00),
(17, 24, 106, '2024-12-23', 3, 8400.00),
(18, 25, 101, '2025-01-12', 3, 2700.00),
(19, 26, 109, '2024-12-19', 1, 4500.00),
(20, 27, 103, '2024-12-15', 1, 1700.00),
(21, 28, 104, '2025-02-10', 3, 6600.00),
(22, 29, 105, '2024-12-09', 1, 2500.00),
(23, 30, 107, '2025-03-01', 1, 3300.00),
(27, 34, 102, '2024-12-20', 1, 1300.00),
(28, 35, 102, '2024-12-27', 2, 2600.00);

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `RoomID` int(11) NOT NULL,
  `RoomType` enum('Standard','Suite','Deluxe') NOT NULL,
  `RoomName` varchar(50) NOT NULL,
  `Price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`RoomID`, `RoomType`, `RoomName`, `Price`) VALUES
(101, 'Standard', 'Standard Room A', 900.00),
(102, 'Standard', 'Standard Room B', 1300.00),
(103, 'Standard', 'Standard Room C', 1700.00),
(104, 'Suite', 'Suite Room A', 2200.00),
(105, 'Suite', 'Suite Room B', 2500.00),
(106, 'Suite', 'Suite Room C', 2800.00),
(107, 'Deluxe', 'Deluxe Room A', 3300.00),
(108, 'Deluxe', 'Deluxe Room B', 3700.00),
(109, 'Deluxe', 'Deluxe Room C', 4500.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `guest`
--
ALTER TABLE `guest`
  ADD PRIMARY KEY (`GuestID`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`ReservationID`),
  ADD KEY `GuestID` (`GuestID`),
  ADD KEY `RoomID` (`RoomID`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`RoomID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `guest`
--
ALTER TABLE `guest`
  MODIFY `GuestID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `ReservationID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`GuestID`) REFERENCES `guest` (`GuestID`),
  ADD CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`RoomID`) REFERENCES `room` (`RoomID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
