-- Database: asimetrix

-- DROP DATABASE asimetrix;


CREATE DATABASE asimetrix
    WITH 
    OWNER = asimetrix
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
CREATE TABLE company (
 id serial ,
 name varchar(45) NOT NULL, 
 user varchar(45) NOT NULL, 
 status int(1)
 PRIMARY KEY (id)
);

CREATE TABLE farm (
  id serial,
  name varchar NOT NULL,
  company_id int,
  status int(1)

  PRIMARY KEY (id),
  CONSTRAINT FK_USER FOREIGN KEY (company_id) REFERENCES company (id) ON DELETE CASCADE
);
CREATE TABLE barn (
  id serial,
  name varchar NOT NULL,
  farm_id int,

  PRIMARY KEY (id),
  CONSTRAINT FK_USER FOREIGN KEY (farm_id) REFERENCES farm (id) ON DELETE CASCADE
);



CREATE TABLE sensor (
  id serial,
  name varchar NOT NULL,
  barn_id int,

  PRIMARY KEY (id),
  CONSTRAINT FK_USER FOREIGN KEY (barn_id) REFERENCES barn (id) ON DELETE CASCADE
);

CREATE TABLE data (
  id serial,
  timestamp varchar NOT NULL,
  value decimal,
  sensor_id int

  PRIMARY KEY (id),
  CONSTRAINT FK_USER FOREIGN KEY (sensor_id) REFERENCES sensor (id) ON DELETE CASCADE
);
