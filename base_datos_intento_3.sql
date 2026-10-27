-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema base_datos_intento_3
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema base_datos_intento_3
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `base_datos_intento_3` DEFAULT CHARACTER SET utf8 ;
USE `base_datos_intento_3` ;

-- -----------------------------------------------------
-- Table `base_datos_intento_3`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `base_datos_intento_3`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(225) NULL,
  `apellido` VARCHAR(225) NULL,
  `email` VARCHAR(225) NULL,
  `password` VARCHAR(225) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `base_datos_intento_3`.`misiones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `base_datos_intento_3`.`misiones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(225) NULL,
  `fecha` VARCHAR(45) NULL,
  `voluntarios_necesarios` VARCHAR(45) NULL,
  `descripcion` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `usuarios_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_misiones_usuarios_idx` (`usuarios_id` ASC) VISIBLE,
  CONSTRAINT `fk_misiones_usuarios`
    FOREIGN KEY (`usuarios_id`)
    REFERENCES `base_datos_intento_3`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
