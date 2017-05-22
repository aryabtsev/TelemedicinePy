#!/bin/bash

sudo apt-get update

sudo apt-get mysql-server
sudo apt-get install  mysql-server

mysql -u root -p BMT4Ever

CREATE TABLE IF NOT EXISTS `mydb`.`Telemedicine` (  `device_id` INT NULL, `heart_rate` INT NULL,   `breath_rate` INT NULL,   `date` DATE NULL,   `time` TIME NULL) ENGINE = InnoDB;