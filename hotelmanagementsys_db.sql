-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2025 at 05:16 PM
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
(17, 'Can add log entry', 5, 'add_logentry'),
(18, 'Can change log entry', 5, 'change_logentry'),
(19, 'Can delete log entry', 5, 'delete_logentry'),
(20, 'Can view log entry', 5, 'view_logentry'),
(21, 'Can add permission', 6, 'add_permission'),
(22, 'Can change permission', 6, 'change_permission'),
(23, 'Can delete permission', 6, 'delete_permission'),
(24, 'Can view permission', 6, 'view_permission'),
(25, 'Can add group', 7, 'add_group'),
(26, 'Can change group', 7, 'change_group'),
(27, 'Can delete group', 7, 'delete_group'),
(28, 'Can view group', 7, 'view_group'),
(29, 'Can add user', 8, 'add_user'),
(30, 'Can change user', 8, 'change_user'),
(31, 'Can delete user', 8, 'delete_user'),
(32, 'Can view user', 8, 'view_user'),
(33, 'Can add content type', 9, 'add_contenttype'),
(34, 'Can change content type', 9, 'change_contenttype'),
(35, 'Can delete content type', 9, 'delete_contenttype'),
(36, 'Can view content type', 9, 'view_contenttype'),
(37, 'Can add session', 10, 'add_session'),
(38, 'Can change session', 10, 'change_session'),
(39, 'Can delete session', 10, 'delete_session'),
(40, 'Can view session', 10, 'view_session');

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
(5, 'admin', 'logentry'),
(7, 'auth', 'group'),
(6, 'auth', 'permission'),
(8, 'auth', 'user'),
(9, 'contenttypes', 'contenttype'),
(1, 'crud', 'adminaccounts'),
(2, 'crud', 'guestaccounts'),
(3, 'crud', 'manageguest'),
(4, 'crud', 'manageroom'),
(10, 'sessions', 'session');

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
(1, 'contenttypes', '0001_initial', '2025-05-31 05:28:57.305281'),
(2, 'auth', '0001_initial', '2025-05-31 05:28:57.706787'),
(3, 'admin', '0001_initial', '2025-05-31 05:28:57.797994'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-05-31 05:28:57.809261'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-05-31 05:28:57.818360'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-05-31 05:28:57.878515'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-05-31 05:28:57.917713'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-05-31 05:28:57.936098'),
(9, 'auth', '0004_alter_user_username_opts', '2025-05-31 05:28:57.946063'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-05-31 05:28:57.979012'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-05-31 05:28:57.982706'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-05-31 05:28:57.995286'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-05-31 05:28:58.010080'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-05-31 05:28:58.024807'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-05-31 05:28:58.038905'),
(16, 'auth', '0011_update_proxy_permissions', '2025-05-31 05:28:58.049925'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-05-31 05:28:58.065568'),
(18, 'crud', '0001_initial', '2025-05-31 05:28:58.378257'),
(19, 'sessions', '0001_initial', '2025-05-31 05:28:58.408508');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `payment_status` varchar(40) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `guest_id_id` int(11) NOT NULL,
  `room_id_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `manageroom_tbl`
--

CREATE TABLE `manageroom_tbl` (
  `room_id` int(11) NOT NULL,
  `room_type` varchar(100) NOT NULL,
  `room_number` varchar(50) NOT NULL,
  `bed_count` int(11) NOT NULL,
  `floor` varchar(50) NOT NULL,
  `room_status` varchar(30) NOT NULL,
  `room_price` decimal(10,2) NOT NULL,
  `available_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `check_in_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

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
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `guestaccounts_tbl`
--
ALTER TABLE `guestaccounts_tbl`
  MODIFY `guest_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `manageguest_tbl`
--
ALTER TABLE `manageguest_tbl`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `manageroom_tbl`
--
ALTER TABLE `manageroom_tbl`
  MODIFY `room_id` int(11) NOT NULL AUTO_INCREMENT;

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
