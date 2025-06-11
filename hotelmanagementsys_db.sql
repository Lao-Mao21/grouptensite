-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 11, 2025 at 05:24 PM
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
-- Database: `hotelmanagementsys_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `adminaccounts_tbl`
--

CREATE TABLE `adminaccounts_tbl` (
  `is_active` tinyint(1) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `first_name` varchar(155) NOT NULL,
  `middle_name` varchar(155) DEFAULT NULL,
  `last_name` varchar(155) NOT NULL,
  `full_name` varchar(310) NOT NULL,
  `username` varchar(150) NOT NULL,
  `verification_token` varchar(255) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `adminaccounts_tbl`
--

INSERT INTO `adminaccounts_tbl` (`is_active`, `admin_id`, `first_name`, `middle_name`, `last_name`, `full_name`, `username`, `verification_token`, `date_of_birth`, `last_login`, `gender`, `email`, `phone_number`, `address`, `password`, `created_at`, `updated_at`) VALUES
(1, 3, 'Man', 'Three', 'Two', '', 'Mn', NULL, '2025-06-11', '2025-06-11 05:49:49.911373', 'male', 'example2@gmail.com', '09155456789', 'One, Two, Three', 'pbkdf2_sha256$600000$rA2gXUKmjT99cfIEMiYc0L$tfHTmffZ2Nm4HRHkscAq4yogF+E2ARbH+9U0ffA1OOc=', '2025-06-11 05:49:17.007602', '2025-06-11 05:49:17.012229'),
(1, 4, 'Jonas', 'E.', 'Admin', '', '2', NULL, '2025-06-11', '2025-06-11 11:44:27.077341', 'male', 'exampleadmin@gmail.com', '09155456789', 'One, Two, Three', 'pbkdf2_sha256$600000$Kpxvj0o2GV5jcFZXcCwNr5$buaRAH7i6oB28UzSuiEGaeWTFZxlvHx8MI6MPeIQlSI=', '2025-06-11 05:57:39.779051', '2025-06-11 05:57:39.788316'),
(1, 5, 'Example', 'S.', 'Sample', '', 'sample', NULL, '2025-06-11', '2025-06-11 06:38:33.184295', 'male', 'example100@gmail.com', '0912222789', 'One, Two, Three', 'pbkdf2_sha256$600000$EN6ruFYzYgSPBWZVaE3nGC$UQjjcAar8wyiP271rFrCqp3FytJYUBLj4Ae1Vh7WVWw=', '2025-06-11 06:38:21.697392', '2025-06-11 06:38:21.701277');

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add admin accounts', 1, 'add_adminaccounts'),
(2, 'Can change admin accounts', 1, 'change_adminaccounts'),
(3, 'Can delete admin accounts', 1, 'delete_adminaccounts'),
(4, 'Can view admin accounts', 1, 'view_adminaccounts'),
(5, 'Can add guest accounts', 2, 'add_guestaccounts'),
(6, 'Can change guest accounts', 2, 'change_guestaccounts'),
(7, 'Can delete guest accounts', 2, 'delete_guestaccounts'),
(8, 'Can view guest accounts', 2, 'view_guestaccounts'),
(9, 'Can add manage guest', 3, 'add_manageguest'),
(10, 'Can change manage guest', 3, 'change_manageguest'),
(11, 'Can delete manage guest', 3, 'delete_manageguest'),
(12, 'Can view manage guest', 3, 'view_manageguest'),
(13, 'Can add manage room', 4, 'add_manageroom'),
(14, 'Can change manage room', 4, 'change_manageroom'),
(15, 'Can delete manage room', 4, 'delete_manageroom'),
(16, 'Can view manage room', 4, 'view_manageroom'),
(17, 'Can add guest archive', 5, 'add_guestarchive'),
(18, 'Can change guest archive', 5, 'change_guestarchive'),
(19, 'Can delete guest archive', 5, 'delete_guestarchive'),
(20, 'Can view guest archive', 5, 'view_guestarchive'),
(21, 'Can add log entry', 6, 'add_logentry'),
(22, 'Can change log entry', 6, 'change_logentry'),
(23, 'Can delete log entry', 6, 'delete_logentry'),
(24, 'Can view log entry', 6, 'view_logentry'),
(25, 'Can add permission', 7, 'add_permission'),
(26, 'Can change permission', 7, 'change_permission'),
(27, 'Can delete permission', 7, 'delete_permission'),
(28, 'Can view permission', 7, 'view_permission'),
(29, 'Can add group', 8, 'add_group'),
(30, 'Can change group', 8, 'change_group'),
(31, 'Can delete group', 8, 'delete_group'),
(32, 'Can view group', 8, 'view_group'),
(33, 'Can add user', 9, 'add_user'),
(34, 'Can change user', 9, 'change_user'),
(35, 'Can delete user', 9, 'delete_user'),
(36, 'Can view user', 9, 'view_user'),
(37, 'Can add content type', 10, 'add_contenttype'),
(38, 'Can change content type', 10, 'change_contenttype'),
(39, 'Can delete content type', 10, 'delete_contenttype'),
(40, 'Can view content type', 10, 'view_contenttype'),
(41, 'Can add session', 11, 'add_session'),
(42, 'Can change session', 11, 'change_session'),
(43, 'Can delete session', 11, 'delete_session'),
(44, 'Can view session', 11, 'view_session');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(6, 'admin', 'logentry'),
(8, 'auth', 'group'),
(7, 'auth', 'permission'),
(9, 'auth', 'user'),
(10, 'contenttypes', 'contenttype'),
(1, 'crud', 'adminaccounts'),
(2, 'crud', 'guestaccounts'),
(5, 'crud', 'guestarchive'),
(3, 'crud', 'manageguest'),
(4, 'crud', 'manageroom'),
(11, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-06-11 03:09:14.653070'),
(2, 'auth', '0001_initial', '2025-06-11 03:09:15.189788'),
(3, 'admin', '0001_initial', '2025-06-11 03:09:15.284575'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-06-11 03:09:15.294245'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-06-11 03:09:15.303394'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-06-11 03:09:15.356929'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-06-11 03:09:15.402345'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-06-11 03:09:15.416859'),
(9, 'auth', '0004_alter_user_username_opts', '2025-06-11 03:09:15.424232'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-06-11 03:09:15.461258'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-06-11 03:09:15.464866'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-06-11 03:09:15.476669'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-06-11 03:09:15.490719'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-06-11 03:09:15.503517'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-06-11 03:09:15.514850'),
(16, 'auth', '0011_update_proxy_permissions', '2025-06-11 03:09:15.523904'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-06-11 03:09:15.534972'),
(18, 'crud', '0001_initial', '2025-06-11 03:09:15.789145'),
(19, 'sessions', '0001_initial', '2025-06-11 03:09:15.820559'),
(20, 'crud', '0002_alter_guestaccounts_email', '2025-06-11 05:28:26.781570');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('4mlcv97fi21azsouvk6hkctx3oosfkmv', '.eJyrVopPLC3JiC8tTi2Kz0xRslIyUdJBFktKTM5OzQNJJBeVpuhBucV6jim5mXmOycn5pXklxU5QRSg6MxKLM4DalGoBDzEjxA:1uPJsZ:FJHvIgoWQ5pvdOCX-1iCZsOaqgWw4kqY3CuapYNMCm4', '2025-06-25 11:44:27.081070'),
('uexklk56j5fg66a6qb31r15q38j9uo0m', '.eJyrVopPLC3JiC8tTi2Kz0xRslIyUdJBFktKTM5OzQNJJBeVpuhBucV6jim5mXmOycn5pXklxU5QRSg6MxKLM4DalGoBDzEjxA:1uPG3d:DXk7OMDABh1Lm9_0NJ1sbfeXSXJsUydWtRChI1s0WRI', '2025-06-25 07:39:37.638400');

-- --------------------------------------------------------

--
-- Table structure for table `guestaccounts_tbl`
--

CREATE TABLE `guestaccounts_tbl` (
  `guest_id` int(11) NOT NULL,
  `first_name` varchar(155) NOT NULL,
  `middle_name` varchar(155) DEFAULT NULL,
  `last_name` varchar(155) NOT NULL,
  `username` varchar(150) NOT NULL,
  `full_name` varchar(310) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `address` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email_verified` tinyint(1) NOT NULL,
  `verification_token` varchar(255) DEFAULT NULL,
  `nationality` varchar(100) DEFAULT NULL,
  `emergency_contact` varchar(100) DEFAULT NULL,
  `notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guestaccounts_tbl`
--

INSERT INTO `guestaccounts_tbl` (`guest_id`, `first_name`, `middle_name`, `last_name`, `username`, `full_name`, `gender`, `email`, `phone_number`, `address`, `password`, `is_active`, `date_of_birth`, `last_login`, `email_verified`, `verification_token`, `nationality`, `emergency_contact`, `notes`, `created_at`, `updated_at`) VALUES
(7, 'Jonas', 'C.', 'Buenavides', 'Lao1Mao', 'Jonas C. Buenavides', 'male', 'example1@gmail.com', '09123456789', 'One, Two, Three', 'pbkdf2_sha256$600000$A18OEmMASabr2Wtl4xQHmZ$I7DEH6qrez205LdHxGO7wuPn3JqMzSKmKmMwV8sswxU=', 1, NULL, NULL, 0, NULL, 'Filipino', 'N/A', '', '2025-06-11 05:48:07.872093', '2025-06-11 05:48:07.872117'),
(8, 'Juan', 'P.', 'Cruz', 'J-one', 'Juan P. Cruz', 'male', 'example2@gmail.com', '0912254789', 'One, Two, Three', 'pbkdf2_sha256$600000$CUcUM6E4iNAh8nT3f5k7KU$JrUHnRv62gwGY6oIFO8awB+Qt2Aoc0eM1iKBzB+JIbI=', 1, NULL, NULL, 0, NULL, 'Filipino', 'N/A', '', '2025-06-11 06:42:07.469008', '2025-06-11 06:42:07.469036'),
(9, 'Example3', 'P.', 'Sample4', 'Mn2', 'Example3 P. Sample4', 'male', 'example100@gmail.com', '09234456789', 'One, Two, Three', 'pbkdf2_sha256$600000$kI2rtKADufB8bh9sPYbslE$6MaXXL5z6jGcLj7TVecfYYjrrNAO+Op1GhjpzBrXxVY=', 1, NULL, NULL, 0, NULL, 'Filipino', 'N/A', '', '2025-06-11 14:35:23.310889', '2025-06-11 14:35:23.310920'),
(10, 'Example2', 'D.', 'Sample2', '22', 'Example2 D. Sample2', 'female', 'example22@gmail.com', '091554456789', 'One, Two, Three', 'pbkdf2_sha256$600000$0Tedx8DhFtPf8HEi9htYGn$RacRP2iS4L9CYOUhY67U6zJijxAM5H0KeTL+zG91wPs=', 1, '2025-07-01', NULL, 0, NULL, 'Filipino', 'N/A', '', '2025-06-11 14:39:21.955440', '2025-06-11 14:39:21.955460');

-- --------------------------------------------------------

--
-- Table structure for table `guestarchive_tbl`
--

CREATE TABLE `guestarchive_tbl` (
  `id` bigint(20) NOT NULL,
  `guest_name` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `guest_count` int(11) NOT NULL,
  `check_in` datetime(6) NOT NULL,
  `check_out` datetime(6) NOT NULL,
  `payment_status` varchar(50) NOT NULL,
  `nationality` varchar(100) NOT NULL,
  `payment_mode` varchar(50) NOT NULL,
  `guest_id_id` int(11) NOT NULL,
  `room_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `manageguest_tbl`
--

CREATE TABLE `manageguest_tbl` (
  `id` bigint(20) NOT NULL,
  `guest_name` varchar(155) NOT NULL,
  `status` varchar(20) NOT NULL,
  `check_in` datetime(6) NOT NULL,
  `check_out` datetime(6) NOT NULL,
  `expected_arrival` datetime(6) NOT NULL,
  `guest_count` int(11) NOT NULL,
  `payment_mode` varchar(20) NOT NULL,
  `payment_status` varchar(40) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `guest_id_id` int(11) NOT NULL,
  `room_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manageguest_tbl`
--

INSERT INTO `manageguest_tbl` (`id`, `guest_name`, `status`, `check_in`, `check_out`, `expected_arrival`, `guest_count`, `payment_mode`, `payment_status`, `created_at`, `updated_at`, `guest_id_id`, `room_id_id`) VALUES
(3, 'Jonas C. Buenavides', 'immediate', '2025-06-11 13:48:00.000000', '2025-06-16 13:48:00.000000', '2025-06-11 13:48:00.000000', 1, 'cash', 'paid', '2025-06-11 05:48:24.334159', '2025-06-11 14:10:44.599313', 7, 1),
(4, 'Juan P. Cruz', 'immediate', '2025-06-11 14:42:00.000000', '2025-06-16 14:42:00.000000', '2025-06-11 14:42:00.000000', 1, 'cash', 'paid', '2025-06-11 06:43:00.136570', '2025-06-11 06:43:00.136582', 8, 2),
(5, 'Example3 P. Sample4', 'immediate', '2025-06-11 23:02:00.000000', '2025-06-26 23:02:00.000000', '2025-06-11 23:02:00.000000', 1, 'cash', 'paid', '2025-06-11 15:03:01.371876', '2025-06-11 15:03:01.371894', 9, 3);

-- --------------------------------------------------------

--
-- Table structure for table `manageroom_tbl`
--

CREATE TABLE `manageroom_tbl` (
  `room_id` int(11) NOT NULL,
  `room_type` varchar(100) NOT NULL,
  `room_number` varchar(50) NOT NULL,
  `bed_count` int(11) NOT NULL,
  `bed_type` varchar(100) NOT NULL,
  `floor` varchar(50) NOT NULL,
  `room_status` varchar(30) NOT NULL,
  `room_price` decimal(10,2) NOT NULL,
  `room_price_type` varchar(100) NOT NULL,
  `available_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `check_in_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manageroom_tbl`
--

INSERT INTO `manageroom_tbl` (`room_id`, `room_type`, `room_number`, `bed_count`, `bed_type`, `floor`, `room_status`, `room_price`, `room_price_type`, `available_at`, `created_at`, `updated_at`, `check_in_id`) VALUES
(1, 'single', '1', 1, 'single', '1', 'occupied', 1500.00, 'custom', '2025-06-11 11:37:00.000000', '2025-06-11 03:37:21.618736', '2025-06-11 14:10:44.602107', NULL),
(2, 'single', '2', 1, 'single', '1', 'occupied', 1500.00, 'custom', '2025-06-11 14:42:00.000000', '2025-06-11 06:42:43.983157', '2025-06-11 06:43:00.144499', NULL),
(3, 'double', '3', 1, 'double', '1', 'occupied', 2400.00, 'custom', '2025-06-11 22:12:00.000000', '2025-06-11 14:12:45.950272', '2025-06-11 15:03:01.400721', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adminaccounts_tbl`
--
ALTER TABLE `adminaccounts_tbl`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `guestaccounts_tbl`
--
ALTER TABLE `guestaccounts_tbl`
  ADD PRIMARY KEY (`guest_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `guestarchive_tbl`
--
ALTER TABLE `guestarchive_tbl`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guestarchive_tbl_guest_id_id_97529e8b_fk_guestacco` (`guest_id_id`),
  ADD KEY `guestarchive_tbl_room_id_id_bc8aa1bb_fk_manageroom_tbl_room_id` (`room_id_id`);

--
-- Indexes for table `manageguest_tbl`
--
ALTER TABLE `manageguest_tbl`
  ADD PRIMARY KEY (`id`),
  ADD KEY `manageguest_tbl_room_id_id_599a40a9_fk_manageroom_tbl_room_id` (`room_id_id`),
  ADD KEY `manageguest_tbl_guest_id_id_7027c86d_fk_guestacco` (`guest_id_id`);

--
-- Indexes for table `manageroom_tbl`
--
ALTER TABLE `manageroom_tbl`
  ADD PRIMARY KEY (`room_id`),
  ADD UNIQUE KEY `room_number` (`room_number`),
  ADD KEY `manageroom_tbl_check_in_id_b2c374f7_fk_manageguest_tbl_id` (`check_in_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adminaccounts_tbl`
--
ALTER TABLE `adminaccounts_tbl`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `guestaccounts_tbl`
--
ALTER TABLE `guestaccounts_tbl`
  MODIFY `guest_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `guestarchive_tbl`
--
ALTER TABLE `guestarchive_tbl`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `manageguest_tbl`
--
ALTER TABLE `manageguest_tbl`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `manageroom_tbl`
--
ALTER TABLE `manageroom_tbl`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `guestarchive_tbl`
--
ALTER TABLE `guestarchive_tbl`
  ADD CONSTRAINT `guestarchive_tbl_guest_id_id_97529e8b_fk_guestacco` FOREIGN KEY (`guest_id_id`) REFERENCES `guestaccounts_tbl` (`guest_id`),
  ADD CONSTRAINT `guestarchive_tbl_room_id_id_bc8aa1bb_fk_manageroom_tbl_room_id` FOREIGN KEY (`room_id_id`) REFERENCES `manageroom_tbl` (`room_id`);

--
-- Constraints for table `manageguest_tbl`
--
ALTER TABLE `manageguest_tbl`
  ADD CONSTRAINT `manageguest_tbl_guest_id_id_7027c86d_fk_guestacco` FOREIGN KEY (`guest_id_id`) REFERENCES `guestaccounts_tbl` (`guest_id`),
  ADD CONSTRAINT `manageguest_tbl_room_id_id_599a40a9_fk_manageroom_tbl_room_id` FOREIGN KEY (`room_id_id`) REFERENCES `manageroom_tbl` (`room_id`);

--
-- Constraints for table `manageroom_tbl`
--
ALTER TABLE `manageroom_tbl`
  ADD CONSTRAINT `manageroom_tbl_check_in_id_b2c374f7_fk_manageguest_tbl_id` FOREIGN KEY (`check_in_id`) REFERENCES `manageguest_tbl` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
