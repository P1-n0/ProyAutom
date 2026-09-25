BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Licencia" (
	"id_licencia"	INTEGER NOT NULL,
	"tipo_licencia"	TEXT NOT NULL,
	"expiracion_anios"	INTEGER NOT NULL,
	PRIMARY KEY("id_licencia")
);
CREATE TABLE IF NOT EXISTS "Usuario" (
	"id_usuario"	INTEGER NOT NULL,
	"nombre"	TEXT NOT NULL,
	"apellido_paterno"	TEXT NOT NULL,
	"apellido_materno"	TEXT NOT NULL,
	"edad"	INTEGER NOT NULL,
	"departamento"	TEXT NOT NULL,
	PRIMARY KEY("id_usuario")
);
CREATE TABLE IF NOT EXISTS "Stock" (
	"id_stock"	INTEGER NOT NULL,
	"marca_monitor"	TEXT,
	"pulgadas_monitor"	INTEGER,
	"marca_teclado"	TEXT,
	"marca_mouse"	TEXT,
	"SN_equipo"	TEXT,
	"marca_equipo"	TEXT,
	"ram_equipo"	INTEGER,
	"almacenamiento_equipo"	INTEGER,
	"procesador_equipo"	TEXT,
	"SO_equipo"	TEXT,
	"id_usuario"	INTEGER NOT NULL,
	"id_licencia"	INTEGER,
	PRIMARY KEY("id_stock"),
	FOREIGN KEY("id_licencia") REFERENCES "Licencia"("id_licencia"),
	FOREIGN KEY("id_usuario") REFERENCES "Usuario"("id_usuario")
);
INSERT INTO "Licencia" ("id_licencia","tipo_licencia","expiracion_anios") VALUES (1,'OEM',15),
 (2,'LTSC',5);
INSERT INTO "Usuario" ("id_usuario", "nombre", "apellido_paterno", "apellido_materno", "edad", "departamento") VALUES 
 (0, 'Bodega', 'General', 'TI', 0, 'Almacen TI'),
 (1, 'Abdiel', 'Peredo', 'Castillo', 21, 'Marketing'),
 (2, 'Enkyl', 'Renteria', 'Chavez', 23, 'RH'),
 (3, 'Michel', 'Valerio', 'Moya', 22, 'Intendencia'),
 (4, 'Josue', 'Chairez', 'Martinez', 21, 'Cafeteria'),
 (5, 'Jesus', 'Pinia', 'Hernandez', 21, 'Nominas');
INSERT INTO "Stock" ("id_stock","marca_monitor","pulgadas_monitor","marca_teclado","marca_mouse","SN_equipo","marca_equipo","ram_equipo","almacenamiento_equipo","procesador_equipo","SO_equipo","id_usuario","id_licencia") VALUES (1,'DELL',27,'HP','DELL','MX2025001',NULL,'HP',512,'i5-8500','Windows 11',1,1),
 (2,'DELL',27,'HP','DELL','MX2025002',NULL,'HP',512,'i5-8500','Windows 11',2,2),
 (3,'DELL',27,'HP','DELL','MX2025003',NULL,'HP',512,'i5-8500','Windows 11',3,1),
 (4,'DELL',27,'HP','DELL','MX2025004',NULL,'DELL',512,'i5-8500','Windows 11',4,2),
 (5,'DELL',27,'HP','DELL','MX2025005',NULL,'DELL',512,'i5-8500','Windows 11',5,1);
COMMIT;
