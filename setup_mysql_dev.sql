create database if not exists Amozol;
CREATE USER IF NOT EXISTS 'zol'@'localhost' IDENTIFIED BY 'Amozol';
GRANT ALL PRIVILEGES ON `Amozol`.* TO 'zol'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'zol'@'localhost';
FLUSH PRIVILEGES;
