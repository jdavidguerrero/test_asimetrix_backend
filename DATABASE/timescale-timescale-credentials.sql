/****  GET STARTED WITH YOUR TIMESCALE CLOUD SERVICE  ****/


/*
SERVICE INFORMATION:

Service name:  timescale
Database name: tsdb
Username:      tsdbadmin
Password:      dm4mztd0jv0uvjla
Service URL:   postgres://tsdbadmin:dm4mztd0jv0uvjla@plo7lhif44.h6oblrgc5x.tsdb.cloud.timescale.com:35696/tsdb?sslmode=require
Port:          35696
*/

----------------------------------------------------------------------------

/*  
 ╔╗
╔╝║
╚╗║
 ║║         CONNECT TO YOUR SERVICE
╔╝╚╦╗
╚══╩╝
 
 ​
1. Install psql:
    https://blog.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/

2. From your command line, run:
    psql "postgres://tsdbadmin:dm4mztd0jv0uvjla@plo7lhif44.h6oblrgc5x.tsdb.cloud.timescale.com:35696/tsdb?sslmode=require"
*/

----------------------------------------------------------------------------

/*
╔═══╗
║╔═╗║
╚╝╔╝║	
╔═╝╔╝	    CREATE A HYPERTABLE
║ ╚═╦╗
╚═══╩╝  
*/

CREATE TABLE conditions (	-- create a regular table
    time        TIMESTAMPTZ       NOT NULL,
    location    TEXT              NOT NULL,
    temperature DOUBLE PRECISION  NULL
);

SELECT create_hypertable('conditions', 'time');	-- turn it into a hypertable

----------------------------------------------------------------------------

/*  
╔═══╗
║╔═╗║
╚╝╔╝║	
╔╗╚╗║      INSERT DATA
║╚═╝╠╗
╚═══╩╝	 
*/

INSERT INTO conditions
  VALUES
    (NOW(), 'office', 70.0),
    (NOW(), 'basement', 66.5),
    (NOW(), 'garage', 77.0);
​
----------------------------------------------------------------------------

/*
FOR MORE DOCUMENTATION AND GUIDES, VISIT	>>>--->	HTTPS://DOCS.TIMESCALE.COM/
*/