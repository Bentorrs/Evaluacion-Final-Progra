-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema ecotechsoluciones
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema ecotechsoluciones
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ecotechsoluciones` DEFAULT CHARACTER SET utf8 ;
USE `ecotechsoluciones` ;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`usuario`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE `ecotechsoluciones`.`usuario` (
  `nombre_usuario` VARCHAR(20) NOT NULL UNIQUE,
  `contrasenna` VARCHAR(255) NOT NULL,
  `es_admin` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`nombre_usuario`),
  UNIQUE INDEX `Nombre_usuario_UNIQUE` (`nombre_usuario` ASC))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`empleados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecotechsoluciones`.`empleados` (
  `id_empleado` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre_empleado` VARCHAR(50) NOT NULL,
  `direccion_empleado` VARCHAR(50) NOT NULL,
  `numero_telefono` VARCHAR(12) NOT NULL,
  `correo_electronico_empleado` VARCHAR(100) NOT NULL,
  `fecha_inicio_contrato` DATETIME NOT NULL,
  `salario_empleado` INT(11) NOT NULL,
  `departamentos_id_departamentos` INT(11) NULL,
  `usuario_nombre_usuario` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_empleado`),
  INDEX `fk_empleados_departamentos1_idx` (`departamentos_id_departamentos` ASC),
  INDEX `fk_empleados_usuario_idx` (`usuario_nombre_usuario` ASC),
  CONSTRAINT `fk_empleados_departamentos1`
    FOREIGN KEY (`departamentos_id_departamentos`)
    REFERENCES `ecotechsoluciones`.`departamentos` (`id_departamentos`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_empleados_usuario`
    FOREIGN KEY (`usuario_nombre_usuario`)
    REFERENCES `ecotechsoluciones`.`usuario` (`nombre_usuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`departamentos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecotechsoluciones`.`departamentos` (
  `id_departamentos` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre_departamento` VARCHAR(45) NOT NULL unique,
  `id_gerente` INT(11) NULL,
  PRIMARY KEY (`id_departamentos`),
  INDEX `fk_departamentos_gerente` (`id_gerente` ASC),
  CONSTRAINT `fk_departamentos_gerente`
    FOREIGN KEY (`id_gerente`)
    REFERENCES `ecotechsoluciones`.`empleados` (`id_empleado`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`proyectos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecotechsoluciones`.`proyectos` (
  `id_proyectos` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre_proyecto` VARCHAR(100) NOT NULL,
  `descripcion_proyecto` VARCHAR(200) NOT NULL,
  `fecha_inicio_proyecto` datetime NOT NULL,
  PRIMARY KEY (`id_proyectos`))
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`proyectos_has_empleados`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecotechsoluciones`.`proyectos_has_empleados` (
  `proyectos_id_proyectos` INT(11) NOT NULL,
  `id_empleado` INT(11) NOT NULL,
  PRIMARY KEY (`proyectos_id_proyectos`, `id_empleado`),
  INDEX `fk_proyectos_has_empleados_empleados1_idx` (`id_empleado` ASC),
  INDEX `fk_proyectos_has_empleados_proyectos1_idx` (`proyectos_id_proyectos` ASC),
  CONSTRAINT `fk_proyectos_has_empleados_empleados1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `ecotechsoluciones`.`empleados` (`id_empleado`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_proyectos_has_empleados_proyectos1`
    FOREIGN KEY (`proyectos_id_proyectos`)
    REFERENCES `ecotechsoluciones`.`proyectos` (`id_proyectos`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`registro_tiempo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ecotechsoluciones`.`registro_tiempo` (
  `id_registro_tiempo` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha_registro` DATE NOT NULL,
  `cantidad_horas_trabajadas` INT(11) NOT NULL,
  `descripcion` VARCHAR(500) NOT NULL,
  `proyectos_id` INT(11) NOT NULL,
  `empleados_id_empleado` INT(11) NOT NULL,
  PRIMARY KEY (`id_registro_tiempo`),
  INDEX `fk_registro_tiempo_proyectos1_idx` (`proyectos_id` ASC),
  INDEX `fk_registro_tiempo_empleados1_idx` (`empleados_id_empleado` ASC),
  CONSTRAINT `fk_registro_tiempo_proyectos1`
    FOREIGN KEY (`proyectos_id`)
    REFERENCES `ecotechsoluciones`.`proyectos` (`id_proyectos`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_registro_tiempo_empleados1`
    FOREIGN KEY (`empleados_id_empleado`)
    REFERENCES `ecotechsoluciones`.`empleados` (`id_empleado`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8;

-- -----------------------------------------------------
-- Table `ecotechsoluciones`.`datos_economicos`
-- -----------------------------------------------------
CREATE OR REPLACE TABLE `ecotechsoluciones`.`datos_economicos` (
  `id_indicador` INT(20) NOT NULL AUTO_INCREMENT,
  `nombre_indicador` VARCHAR(100) NOT NULL,
  `fecha` DATETIME NOT NULL,
  `fecha_consulta` DATETIME NOT NULL,
  `usuario_nombre_usuario` VARCHAR(20) NOT NULL,
  `sitio_origen` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id_indicador`),
  INDEX `fk_indicadores_usuario_idx` (`usuario_nombre_usuario` ASC),
  CONSTRAINT `fk_indicadores_usuario`
    FOREIGN KEY (`usuario_nombre_usuario`)
    REFERENCES `ecotechsoluciones`.`usuario` (`nombre_usuario`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
) ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
