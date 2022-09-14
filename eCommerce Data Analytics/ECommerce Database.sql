CREATE TABLE `Dim_Date` (
  `dateKey` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `dateNum` date NOT NULL,
  `monthNum` int NOT NULL,
  `monthName` varchar(10) NOT NULL,
  `monthShortName` varchar(4) NOT NULL,
  `dayNum` int NOT NULL,
  `dayOfWeek` int NOT NULL,
  `yearNum` int NOT NULL,
  `quarter` int NOT NULL
);

CREATE TABLE `Dim_Product` (
  `productKey` bigint PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `productId` bigint NOT NULL,
  `categoryId` bigint NOT NULL,
  `categoryName` varchar(128),
  `price` float8 NOT NULL,
  `brand` varchar(50),
  `activeFlag` boolean DEFAULT True
);

CREATE TABLE `Dim_Event_Type` (
  `eventType` varchar(30) PRIMARY KEY
);

CREATE TABLE `Fact_Product` (
  `productKey` bigint NOT NULL,
  `dateKey` bigint NOT NULL,
  `event_type` varchar(30) NOT NULL,
  `counter` bigint DEFAULT 1,
  PRIMARY KEY (`productKey`, `dateKey`, `event_type`)
);

ALTER TABLE `Fact_Product` ADD FOREIGN KEY (`productKey`) REFERENCES `Dim_Product` (`productKey`);

ALTER TABLE `Fact_Product` ADD FOREIGN KEY (`dateKey`) REFERENCES `Dim_Date` (`dateKey`);

ALTER TABLE `Fact_Product` ADD FOREIGN KEY (`event_type`) REFERENCES `Dim_Event_Type` (`eventType`);
