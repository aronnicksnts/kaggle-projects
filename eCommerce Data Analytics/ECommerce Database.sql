CREATE TABLE `Dim_Date` (
  `dateKey` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `dateNum` datetime NOT NULL,
  `monthNum` int NOT NULL,
  `monthName` varchar(10) NOT NULL,
  `monthShortName` varchar(4) NOT NULL,
  `dayNum` int NOT NULL,
  `dayOfWeek` int NOT NULL,
  `yearNum` int NOT NULL,
  `quarter` int NOT NULL
);

CREATE TABLE `Dim_Product` (
  `productKey` int PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `productId` int NOT NULL,
  `categoryId` int NOT NULL,
  `categoryName` varchar(128),
  `price` int NOT NULL,
  `brand` varchar(50),
  `activeFlag` boolean DEFAULT True
);

CREATE TABLE `Fact_Product` (
  `productKey` int NOT NULL,
  `dateKey` int NOT NULL,
  `event_type` varchar(30) NOT NULL,
  `counter` int DEFAULT 1,
  PRIMARY KEY (`productKey`, `dateKey`)
);

ALTER TABLE `Fact_Product` ADD FOREIGN KEY (`productKey`) REFERENCES `Dim_Product` (`productKey`);

ALTER TABLE `Fact_Product` ADD FOREIGN KEY (`dateKey`) REFERENCES `Dim_Date` (`dateKey`);
