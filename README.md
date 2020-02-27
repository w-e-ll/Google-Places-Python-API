# Google Places API Python Scraper

The Places API is a service that returns information about places using HTTP requests. Places are defined within this API as establishments, geographic locations, or prominent points of interest.
It scrapes hotel descriptions, names, lat, long, id, and other stuff from https://maps.googleapis.com/maps/api/place/. 
Scraped data stored in PostgreSQL database.

#### Introducing the API
The following place requests are available:

- Place Search returns a list of places based on a user's location or search string.
- Place Details returns more detailed information about a specific place, including user reviews.
- Place Photos provides access to the millions of place-related photos stored in Google's Place database.
- Place Autocomplete automatically fills in the name and/or address of a place as users type.
- Query Autocomplete provides a query prediction service for text-based geographic searches, returning suggested queries as users type.
Each of the services is accessed as an HTTP request, and returns either an JSON or XML response. All requests to a Places service must use the https:// protocol, and include an API key.

The Places API uses a place ID to uniquely identify a place. For details about the format and usage of this identifier across the Places API and other APIs, see the Place IDs documentation.


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
instractions: https://lite.ip2location.com/database/ip-country-region-city-latitude-longitude-zipcode-timezone

## Import the database:
- COPY ip2location_db11 FROM 'IP2LOCATION-LITE-DB11.CSV' WITH CSV QUOTE AS '"';

* Now open api_keys.py and insert your Google Places API into the variable.
* Run: python google_places_api.py --help and you will see:

usage: python google_places_api.py [-h] [--country] [--city] [--word] [--radius] [--do] [--rownumber]

optional arguments:
 * -h, --help    show this help message and exit
 * --country     Input a country code (like "US" or "FR" or "NZ"), or "ALL" for all countries
 * --city        Enter a city name (like "New York" or "Berlin" or "Moscow")
 * --word        Enter a keyword
 * --radius      Enter a radius between 0 and 50000 (default is 10000)
 * --do          Enter next arguments: "show" or "save"
 * --rownumber   Input a specific row number 

made by: https://w-e-ll.com
