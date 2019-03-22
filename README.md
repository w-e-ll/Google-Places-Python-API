# Google Places API Python Scraper

Python spyder scrapes hotel data (place_id, hotel_name, address, latitude, longitude, country) from Google Places API service, saves results in PostgrteSQL Database.


## To install requirements and start the application:

* virtualenv -p python3.6 google_places_api
* cd google_places_api
* activate it (source bin/activate)
* git clone https://github.com/w-e-ll/Google-Places-Python-API.git
* cd Google-Places-Python-API
* pip install -r requirements.txt
* Download and install DB11 (IP2Location™ LITE IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE Database) from here (https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone), follow the instruction on the same download page and you will have the DB imported into PostgreSQL in a minute.
* Then make install: pip install json argparse time psycopg2 datetime decimal colorama
* Configure PostgreSQL.

## Create Table:

CREATE DATABASE ip2location WITH ENCODING 'UTF8';
\c ip2location
CREATE TABLE ip2location_db11(
	ip_from bigint NOT NULL,
	ip_to bigint NOT NULL,
	country_code character(2) NOT NULL,
	country_name character varying(64) NOT NULL,
	region_name character varying(128) NOT NULL,
	city_name character varying(128) NOT NULL,
	latitude real NOT NULL,
	longitude real NOT NULL,
	zip_code character varying(30) NOT NULL,
	time_zone character varying(8) NOT NULL,
	CONSTRAINT ip2location_db11_pkey PRIMARY KEY (ip_from, ip_to)
);

## Import the database:
- COPY ip2location_db11 FROM 'IP2LOCATION-LITE-DB11.CSV' WITH CSV QUOTE AS '"';

* Now open api_keys.py and insert your Google Places API into the variable.
* Run: python google_places_api.py --help and you will see:

usage: python google_places_api.py [-h] [--country] [--city] [--word] [--radius]
                  [--do] [--rownumber]

optional arguments:
  -h, --help    show this help message and exit
  --country     Input a country code (like "US" or "FR" or "NZ"), or "ALL" for all countries
  --city        Enter a city name (like "New York" or "Berlin" or "Moscow")
  --word        Enter a keyword
  --radius      Enter a radius between 0 and 50000 (default is 10000)
  --do          Enter next arguments: "show" or "save"
  --rownumber   Input a specific row number 

made by: https://w-e-ll.com/cv/
