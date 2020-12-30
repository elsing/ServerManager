-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 195.201.95.187
-- Generation Time: Sep 29, 2018 at 09:14 PM
-- Server version: 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.1.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `servermanager`
--

-- --------------------------------------------------------

--
-- Table structure for table `devices`
--

CREATE TABLE `devices` (
  `serverID` int(200) NOT NULL,
  `userID` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `IP` varchar(20) NOT NULL,
  `type` varchar(20) NOT NULL,
  `brand` varchar(30) NOT NULL,
  `productline` varchar(30) NOT NULL,
  `purpose` text NOT NULL,
  `cpus` varchar(30) NOT NULL,
  `ram` varchar(30) NOT NULL,
  `psus` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `devices`
--

INSERT INTO `devices` (`serverID`, `userID`, `name`, `IP`, `type`, `brand`, `productline`, `purpose`, `cpus`, `ram`, `psus`) VALUES
(223880131, 337965876, 'pfSense', '10.10.10.1', 'Server', 'VMware', 'N/A', 'Runs a firewall for the VMs and VPN.', 'Duel Xeon', '2GB', 'N/A'),
(256759103, 337965876, 'Windows Server 2016 AD', '10.10.10.5', 'Server', 'VMware', 'N/A', 'This is the server that provides all the other servers with Active Directory.', 'Duel Xeon', '4GB', 'N/A'),
(829023988, 337965876, 'Windows Server 2012 Axigen', '10.10.10.223', 'Server', 'VMware', 'N/A', 'Runs a Axigen Mail server.', 'Dual Xeon', '4GB', 'N/A');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `devices`
--
ALTER TABLE `devices`
  ADD PRIMARY KEY (`serverID`),
  ADD KEY `userID` (`userID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `devices`
--
ALTER TABLE `devices`
  ADD CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
