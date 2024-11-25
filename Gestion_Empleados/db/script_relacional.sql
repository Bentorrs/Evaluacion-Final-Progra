-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema gestion_empleados
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS gestion_empleados;
-- -----------------------------------------------------
-- Schema gestion_empleados
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `gestion_empleados` DEFAULT CHARACTER SET utf8 ;
USE `gestion_empleados` ;

-- -----------------------------------------------------
-- Table `gestion_empleados`.`DEPARTAMENTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`DEPARTAMENTO` (
  `id_departamento` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL,
  PRIMARY KEY (`id_departamento`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`USUARIO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`USUARIO` (
  `nombre_usuario` VARCHAR(100) NOT NULL,
  `contraseña` VARCHAR(100) NULL,
  PRIMARY KEY (`nombre_usuario`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`EMPLEADO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`EMPLEADO` (
  `id_empleado` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NULL,
  `direccion` VARCHAR(100) NULL,
  `telefono` VARCHAR(20) NULL,
  `correo` VARCHAR(100) NULL,
  `fecha_contrato` DATE NULL,
  `salario` INT NULL,
  `DEPARTAMENTO_id_departamento` INT NOT NULL,
  `USUARIO_nombre_usuario` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_empleado`),
  INDEX `fk_EMPLEADO_DEPARTAMENTO1_idx` (`DEPARTAMENTO_id_departamento` ASC) ,
  INDEX `fk_EMPLEADO_USUARIO1_idx` (`USUARIO_nombre_usuario` ASC) ,
  CONSTRAINT `fk_EMPLEADO_DEPARTAMENTO1`
    FOREIGN KEY (`DEPARTAMENTO_id_departamento`)
    REFERENCES `gestion_empleados`.`DEPARTAMENTO` (`id_departamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_EMPLEADO_USUARIO1`
    FOREIGN KEY (`USUARIO_nombre_usuario`)
    REFERENCES `gestion_empleados`.`USUARIO` (`nombre_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`PROYECTO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`PROYECTO` (
  `id_proyecto` INT NOT NULL AUTO_INCREMENT,
  `nombre_proyecto` VARCHAR(100) NULL,
  `descripcion` VARCHAR(100) NULL,
  `fecha_inicio` DATE NULL,
  PRIMARY KEY (`id_proyecto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`TIEMPO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`TIEMPO` (
  `id_tiempo` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL,
  `horas` DATETIME NULL,
  `descripcion` VARCHAR(100) NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_tiempo`),
  INDEX `fk_TIEMPO_EMPLEADO1_idx` (`id_empleado` ASC) ,
  UNIQUE INDEX `EMPLEADO_id_empleado_UNIQUE` (`id_empleado` ASC) ,
  CONSTRAINT `fk_TIEMPO_EMPLEADO1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `gestion_empleados`.`EMPLEADO` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`PROYECTO_has_EMPLEADO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`PROYECTO_has_EMPLEADO` (
  `PROYECTO_id_proyecto` INT NOT NULL,
  `EMPLEADO_id_empleado` INT NOT NULL,
  PRIMARY KEY (`PROYECTO_id_proyecto`, `EMPLEADO_id_empleado`),
  INDEX `fk_PROYECTO_has_EMPLEADO_EMPLEADO1_idx` (`EMPLEADO_id_empleado` ASC) ,
  INDEX `fk_PROYECTO_has_EMPLEADO_PROYECTO1_idx` (`PROYECTO_id_proyecto` ASC) ,
  CONSTRAINT `fk_PROYECTO_has_EMPLEADO_PROYECTO1`
    FOREIGN KEY (`PROYECTO_id_proyecto`)
    REFERENCES `gestion_empleados`.`PROYECTO` (`id_proyecto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_PROYECTO_has_EMPLEADO_EMPLEADO1`
    FOREIGN KEY (`EMPLEADO_id_empleado`)
    REFERENCES `gestion_empleados`.`EMPLEADO` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `gestion_empleados`.`ADMINISTRADOR`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gestion_empleados`.`ADMINISTRADOR` (
  `EMPLEADO_id_empleado` INT NOT NULL,
  `nombre_admin` VARCHAR(100) NOT NULL,
  INDEX `fk_ADMINISTRADOR_EMPLEADO1_idx` (`EMPLEADO_id_empleado` ASC) ,
  PRIMARY KEY (`EMPLEADO_id_empleado`),
  CONSTRAINT `fk_ADMINISTRADOR_EMPLEADO1`
    FOREIGN KEY (`EMPLEADO_id_empleado`)
    REFERENCES `gestion_empleados`.`EMPLEADO` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
