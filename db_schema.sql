CREATE USER 'pkujishi'@'localhost' IDENTIFIED BY 'jishipku';
GRANT ALL PRIVILEGES ON pkujishi . * TO 'pkujishi'@'localhost';
CREATE DATABASE pkujishi
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;
