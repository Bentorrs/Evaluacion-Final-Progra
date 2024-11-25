use ecotechsoluciones;

--INSERT INTO departamentos (id_departamentos, nombre_departamento)
--VALUES (9, 'Recursos Humanos');

--INSERT INTO departamentos (id_departamentos, nombre_departamento)
--VALUES (10, 'Ventas');

--INSERT INTO usuario (nombre_usuario, contrasenna, es_admin)
--VALUES ('pedro123', '123', 0);

--INSERT INTO empleados (nombre_empleado, direccion_empleado, numero_telefono, correo_electronico_empleado, 
--    fecha_inicio_contrato, salario_empleado, departamentos_id_departamentos, usuario_nombre_usuario)
--VALUES ('Pedro', 'Valdivia', '912345', 'pedro@gmail.com', '2024-01-10', 30000, 10, 'pedro123');

INSERT INTO usuario (nombre_usuario, contrasenna, es_admin)
VALUES ('admin123', '098f6bcd4621d373cade4e832627b4f6', 1);

INSERT INTO empleados (nombre_empleado, direccion_empleado, numero_telefono, correo_electronico_empleado, 
    fecha_inicio_contrato, salario_empleado, departamentos_id_departamentos, usuario_nombre_usuario)
VALUES ('Benja', 'Los Lagos', '96789', 'benja@gmail.com', '2024-01-10', 40000, 9, 'sarten123');