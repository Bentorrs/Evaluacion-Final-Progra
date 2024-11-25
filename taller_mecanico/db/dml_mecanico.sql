use taller_mecanico;
-- Ingreso de un mecanico
insert into	persona(id_persona, nombre, apellido) values (1, 'Juan', 'Perez');
insert into mecanico(id_mecanico, valor_honorario, id_persona) values (1, 20000, 1);
commit;
-- Comprobar
--select * from persona;
--select * from mecanico;
-- Ingreso de un mecanico con id automatico
insert into	persona(nombre, apellido) values ('Ana', 'Rojas');
insert into mecanico(valor_honorario, id_persona) values (20000, 2);
commit;
-- Mostar mecanicos con sus datos de persona mediante equi-join
--select nombre, apellido, valor_honorario from persona, mecanico 
--where persona.id_persona = mecanico.id_persona;
-- Modificar valor de honorario de Juan Perez
--dselect id_persona from persona where nombre = 'Juan' and apellido = 'Perez';
update mecanico set valor_honorario = 22000 where id_persona = 1;
commit;
-- Eliminar registro de Juan Perez
--select id_persona from persona where nombre = 'Juan' and apellido = 'Perez';
--delete from mecanico where id_persona = 1;
--delete from persona where id_persona = 1;
--commit;
-- Creacion de clientes y sus vehiculos
insert into persona (id_persona, nombre, apellido) values (3, 'Armando', 'Pleito');
insert into cliente (id_cliente, telefono, id_persona) values (3, '+5691234', 3);
insert into vehiculo (patente_vehiculo, marca, modelo, agno, id_cliente)
values ('XXX123', 'Nissan', 'V16', 1995, 3);
commit;
