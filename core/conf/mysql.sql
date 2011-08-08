SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `enrico` DEFAULT CHARACTER SET latin1 ;
USE `enrico` ;

-- -----------------------------------------------------
-- Table `enrico`.`docs`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`docs` (
  `docid` VARCHAR(45) NOT NULL ,
  `triple` INT(11) NOT NULL ,
  `count` INT(11) NOT NULL ,
  PRIMARY KEY (`docid`, `triple`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`entities`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`entities` (
  `id` INT(11) NOT NULL ,
  `oc_id` VARCHAR(200) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `oc_id_UNIQUE` (`oc_id` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 2261
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`keywords`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`keywords` (
  `id` INT(11) NOT NULL ,
  `keyword` VARCHAR(200) NOT NULL ,
  `docid` VARCHAR(45) NOT NULL ,
  `count` INT(11) NOT NULL ,
  PRIMARY KEY (`id`, `docid`, `keyword`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`pages_index`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`pages_index` (
  `docid` VARCHAR(45) NOT NULL ,
  `ind_date` DATETIME NOT NULL ,
  PRIMARY KEY (`docid`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`triples`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`triples` (
  `id` INT(11) NOT NULL ,
  `subject` VARCHAR(200) NULL DEFAULT NULL ,
  `verb` VARCHAR(200) NULL DEFAULT NULL ,
  `object` VARCHAR(200) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `triple_UNIQUE` (`subject` ASC, `verb` ASC, `object` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 3138
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`expansion`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`expansion` (
  `docid` VARCHAR(50) NOT NULL ,
  `triple` INT NOT NULL ,
  `score` DECIMAL(11,10)  NULL ,
  PRIMARY KEY (`docid`, `triple`) ,
  INDEX `fk_expansion_triples1` (`triple` ASC) ,
  CONSTRAINT `fk_expansion_triples1`
    FOREIGN KEY (`triple` )
    REFERENCES `enrico`.`triples` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `enrico`.`doc_sim`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`doc_sim` (
  `doc1` VARCHAR(50) NOT NULL ,
  `doc2` VARCHAR(50) NOT NULL ,
  `score` DECIMAL(12,10) NOT NULL ,
  PRIMARY KEY (`doc1`, `doc2`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `enrico`.`word_count`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `enrico`.`word_count` (
  `count` INT NOT NULL ,
  `word` VARCHAR(200) NOT NULL ,
  PRIMARY KEY (`word`) )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
