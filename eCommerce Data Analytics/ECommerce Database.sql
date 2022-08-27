CREATE TABLE `category` (
  `category_id` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `category_parent` bigint,
  `category_name` varchar(30) UNIQUE,
  `category_active` boolean DEFAULT true
);

CREATE TABLE `brand` (
  `brand_id` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(30) UNIQUE,
  `brand_active` boolean DEFAULT true
);

CREATE TABLE `event_type` (
  `event_type_id` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `event_type_name` varchar(16)
);

CREATE TABLE `product` (
  `product_id` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255),
  `product_price` double NOT NULL,
  `brand_id` bigint,
  `product_active` boolean DEFAULT true,
  `product_viewed` int DEFAULT 0,
  `product_added_cart` int DEFAULT 0,
  `product_removed_cart` int DEFAULT 0,
  `product_purchased` int DEFAULT 0
);

CREATE TABLE `user` (
  `user_id` bigint PRIMARY KEY NOT NULL,
  `user_name` varchar(255),
  `user_active` boolean DEFAULT true,
  `user_spent` double DEFAULT 0,
  `user_total_active_time` int DEFAULT 0
);

CREATE TABLE `user_session` (
  `user_session_id` char(36) PRIMARY KEY NOT NULL,
  `user_id` bigint,
  `user_session_start_time` datetime DEFAULT null,
  `user_session_end_time` datetime DEFAULT null,
  `user_session_active` boolean DEFAULT true
);

CREATE TABLE `user_activity` (
  `user_activity_id` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `event_time` datetime,
  `event_type_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `category_id` bigint,
  `user_id` bigint NOT NULL,
  `user_session_id` char(36) NOT NULL,
  `user_activity_active` boolean DEFAULT true
);

ALTER TABLE `category` ADD FOREIGN KEY (`category_parent`) REFERENCES `category` (`category_id`);

ALTER TABLE `product` ADD FOREIGN KEY (`brand_id`) REFERENCES `brand` (`brand_id`);

ALTER TABLE `user_session` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `user_activity` ADD FOREIGN KEY (`event_type_id`) REFERENCES `event_type` (`event_type_id`);

ALTER TABLE `user_activity` ADD FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

ALTER TABLE `user_activity` ADD FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`);

ALTER TABLE `user_activity` ADD FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `user_activity` ADD FOREIGN KEY (`user_session_id`) REFERENCES `user_session` (`user_session_id`);
