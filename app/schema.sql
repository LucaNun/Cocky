CREATE TABLE `ingredients` ( 
  `ingredientsID` INT AUTO_INCREMENT NOT NULL,
  `pumpID` SMALLINT NULL,
  `alcohol` BOOL NOT NULL,
  `manual` BOOL NOT NULL,
  `name` VARCHAR(250) NOT NULL,
   PRIMARY KEY (`ingredientsID`)
);

CREATE TABLE `mixtures` ( 
  `mixturesID` INT AUTO_INCREMENT NOT NULL,
  `name` VARCHAR(250) NOT NULL,
  `description` TINYTEXT NULL,
   PRIMARY KEY (`mixturesID`)
);

CREATE TABLE `mixtureContents` ( 
  `ingredientsID` INT NOT NULL,
  `mixturesID` INT NOT NULL,
  `amount` SMALLINT NOT NULL
);

CREATE TABLE `pumps` ( 
  `pumpID` SMALLINT AUTO_INCREMENT NOT NULL,
  `pin` TINYINT NOT NULL,
   PRIMARY KEY (`pumpID`)
);

ALTER TABLE `ingredients` ADD CONSTRAINT `FK_ingredients_pumpID` FOREIGN KEY (`pumpID`) REFERENCES `pumps` (`pumpID`);

ALTER TABLE `mixtureContents` ADD CONSTRAINT `FK_mixtureContents_mixturesID` FOREIGN KEY (`mixturesID`) REFERENCES `mixtures` (`mixturesID`);
ALTER TABLE `mixtureContents` ADD CONSTRAINT `FK_mixtureContents_ingredientsID` FOREIGN KEY (`ingredientsID`) REFERENCES `ingredients` (`ingredientsID`);


INSERT INTO `ingredients` (`ingredientsID`, `pumpID`, `alcohol`, `manual`, `name`) VALUES
('1','1','1','0','Gin'),
('2', Null,'0','1','Eiswürfel'),
('3', Null,'0','1','Limettenscheibe'),
('4', Null,'0','1','Gurkenscheibe'),
('5','2','0','0','Tonic Water'),
('6','3','1','0','Ginger Bier'),
('7','4','0','0','Limettensaft'),
('8','5','1','0','Wodka');

INSERT INTO `mixtures` (`mixturesID`, `name`, `description`) VALUES 
('1','Gin Tonic','Gin mit Tonicwater mit Gurke'),
('2','Moscow Mule','...........');

INSERT INTO `mixtureContents` (`mixturesID`, `ingredientsID`, `amount`) VALUES
(1,1,40),
(1,5,60),
(2,6,20),
(2,7,10),
(2,2,2),
(2,4,2),
(2,8,70);

INSERT INTO `pumps` (`pumpID`, `pin`) VALUES
('1','24'),(2, 21),(3, 26),(4, 19),(5, 13),(6, 23),(7, 25),(8, 12),(9, 16),(10, 20);













