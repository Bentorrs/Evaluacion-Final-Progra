-- c:\xampp\mysql\bin\mysql -u root < db\script_usuario.sql
USE taller_mecanico;

DROP TABLE IF EXISTS usuario;

CREATE TABLE usuario (
    nombre_usuario VARCHAR(50) NOT NULL PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    es_admin TINYINT(1) NOT NULL DEFAULT 0
);

INSERT INTO usuario VALUES('admin', 'admin', 1);
INSERT INTO usuario VALUES('user', 'user', 0);
COMMIT;
