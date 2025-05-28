-- Dar permisos al usuario root para conectarse desde cualquier host
ALTER USER 'root'@'%' IDENTIFIED BY '1092';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES; 