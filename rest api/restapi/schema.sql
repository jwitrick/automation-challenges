DROP TABLE IF EXISTS `words`;
        
CREATE TABLE `words` (
  `word` VARCHAR(255) NOT NULL DEFAULT 'NULL',
  `count` MEDIUMINT NOT NULL,
  PRIMARY KEY (`word`)
);
