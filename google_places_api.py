# -*- coding: UTF-8 -*-
import sys
import json
import time
import psycopg2
import argparse
import datetime
import urllib.parse
import urllib.request
import requests
from time import gmtime, strftime
from colorama import init

init(autoreset=True)

# Enter here your Google Places API key
APIKeys = [
    'AIzaSyBrppSzYOTTUS1zr4-w1hKL3xi0OLBzt8Q',
    'AIzaSyA3owG1nBiRJNcruZFUiWYIAO1Np5eqblo',
    'AIzaSyCeoqRxih9OCxppTLS6EOVvjEU6VqXkmE0',
    'AIzaSyCghf2LRvYd4N7-VjSiEDE3VCMruZToyx4',
    'AIzaSyBjW4M9hD_PtPZg9-DrGjWO3ZbUzKqRpOA',
    'AIzaSyA-brjbRZZacVWNHSZ-bD30Zo75kHFLFG0',
    'AIzaSyAbm3R7u0gZzodN-z0yRPRcWBLnYRrFxEA',
    'AIzaSyDlmKADESKX7jNvpRJX-qAciuKlNk6w60g',
    'AIzaSyBQDE4sD83tmowk12_kvlOL0C1vNHPJzOs',
    'AIzaSyC3zOTlCl6eeL86kLOiWyYODj-Yw3roUEo',
    'AIzaSyA6JqQPkFH76e4mixKjZ3GFkfeIGz1RA1w',
    'AIzaSyBRf83XA1op3q9t2rH_YSpn4rSkUPn1VHA',
    'AIzaSyB3vUVxJQk3qYyrEbLuMPaQI-MKXeZam-I',
    'AIzaSyB_xmI-HlTGubYsnmg5vl9HyjIaNoSGtPQ',
    'AIzaSyA3owG1nBiRJNcruZFUiWYIAO1Np5eqblo',
]

# Here we organize the choices command line aruments
parser = argparse.ArgumentParser()
parser.add_argument('--country', dest='country', type=str,
                    help="input a country code (like \"US\" or \"FR\" or \"RU\")", metavar='')
parser.add_argument('--city', dest='city', type=str,
                    help="enter a city name (like \"New York\" or \"Paris\" or \"Auckland\")", metavar='')
parser.add_argument('--word', dest='word', default='movie_theater', type=str,
                    help="enter a keyword", metavar='')
parser.add_argument('--radius', dest='radius', default='25000', type=int,
                    help="enter a radius between 0 and 50000 (default is 25000)", metavar='')
parser.add_argument('--do', dest='do', default='show', type=str, choices=['show', 'save'],
                    help="arguments are \"show\" or \"save\"", metavar='')  # Option: --SQL statement
parser.add_argument('--rownumber', dest='rownumber', type=int, help="input a specific row number", metavar='')
args = parser.parse_args()

#####################################################################

print()
print(' !!! => We got: {} keys left... :)'.format(len(APIKeys)))

# Enter here your database credentials
Connection_Details = "dbname='ip2location' user='postgres' host='localhost' password='1122' port='5432'"

#####################################################################

long_field = {}
short_field = {}


def get_place_for_show(countdown_order, latitude, longitude, city_name, country_code):

    # Google call for Place_ID
    url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

    params1 = {'location': '%s,%s' % (latitude, longitude),
               'radius': '%s' % args.radius,
               'keyword': '%s' % args.word,
               'key': APIKeys[0]}

    # Get response by url1
    response1 = requests.get(url=url1, params=params1)
    response_data1 = response1.json()
    if response_data1['status'] == 'OVER_QUERY_LIMIT':
        del APIKeys[0]

    print('=== Getting response from nearby search endpoint => MAX 60 places !!! ===')

    while True:
        # Google call for Place_next_page_token
        results = response_data1.get("results", None)
        page_token = response_data1.get("next_page_token", None)

        # Here we go to store JSON elements for SQL
        if response_data1['status'] == 'ZERO_RESULTS':
            print("\033[91m" + '{0}) Nothing found for: {1}, {2} at {3}'.format(
                countdown_order, city_name, country_code, datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'), "\033[0m"))
            time.sleep(2)

        elif response_data1['status'] == 'REQUEST_DENIED':
            del APIKeys[0]
            print(' => Request Denied... Poped first used key...')
            continue

        # Google call for place_id
        elif response_data1['status'] == 'OK':

            # Retrieve every placeid
            for i in results:
                SQL_Place_ID = i['place_id']
                url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'
                params2 = {'placeid': SQL_Place_ID,
                           'key': APIKeys[0]}

                # Get response by url2
                response2 = requests.get(url=url2, params=params2)
                response_data2 = response2.json()
                if response_data2['status'] == 'OVER_QUERY_LIMIT':
                    del APIKeys[0]
                # if data retrieved correctly
                if response_data2['status'] == 'OK':
                    result = response_data2.get("result", None)
                    place_id = result.get("place_id", None)
                    hotel_name = result.get("name", None)
                    address = result.get("formatted_address", None)
                    latitude = result['geometry']['location'].get("lat", None)
                    longitude = result['geometry']['location'].get("lng", None)
                    country = str(result.get("formatted_address", None)).split(", ")[-1]
                    print("\033[92m" + '+' + "\033[0m", hotel_name + ':', address, ',', '(', latitude, ',', longitude, ')')

        time.sleep(2)
        # if there is the next page token, so work it out
        url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        params1 = {'location': '%s,%s' % (latitude, longitude),
                   'radius': '%s' % args.radius,
                   'keyword': '%s' % args.word,
                   'key': APIKeys[0],
                   'pagetoken': page_token}
        # Get response by url1
        response1 = requests.get(url=url1, params=params1)
        response_data1 = response1.json()
        if response_data1['status'] == 'OVER_QUERY_LIMIT':
            del APIKeys[0]
        print('=== Getting next page from nearby search endpoint ===============>')

        if page_token == None:
            print("=== No more page token || BREAK ===")
            break

    # The end of current search
    print("\033[92m" + '{0}) Total Places found: {1} near: {2}, {3} at {4}'.format(
        countdown_order, len(results), city_name, country_code,
        datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), "\033[0m"))


def get_place_for_save(countdown_order, latitude, longitude, city_name, country_code):

    # Connect to postgres
    connection2 = psycopg2.connect(Connection_Details)
    cursor2 = connection2.cursor()
    print('=== Connection2 established ===')

    # Connect to postgres
    connection3 = psycopg2.connect(Connection_Details)
    cursor3 = connection3.cursor()
    print('=== Connection3 established ===')

    # Google call for place_id
    url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    params1 = {'location': '%s,%s' % (latitude, longitude),
               'radius': '%s' % args.radius,
               'keyword': '%s' % args.word,
               'key': APIKeys[0]}

    # Get response by url1
    response1 = requests.get(url=url1, params=params1)
    response_data1 = response1.json()
    if response_data1['status'] == 'OVER_QUERY_LIMIT':
        del APIKeys[0]
    print('=== Getting response from nearby search endpoint => MAX 60 places !!! ===')

    # Inserting data into database
    sqlStatement = "INSERT INTO hoteldetails ( \
                      place_id, hotel_name, address, latitude, longitude, country) \
                      VALUES (%s, %s, %s, %s, %s, %s)"

    # Here we go to store JSON elements for SQL
    while True:
        # get results
        results = response_data1.get("results", None)
        page_token = response_data1.get("next_page_token", None)

        # Here we go to store JSON elements for SQL
        if response_data1['status'] == 'ZERO_RESULTS':
            print("\033[91m" + '{0}) Nothing found for: {1}, {2} at {3}'.format(
                countdown_order, city_name, country_code, datetime.datetime.now().strftime(
                    '%Y-%m-%d %H:%M:%S'), "\033[0m"))
            time.sleep(2)

        # if data retrieved correctly
        elif response_data1['status'] == 'OK':
            print('=== Getting placeid ===')
            for i in results:
                SQL_Place_ID = i['place_id']

                # retrieve placeid from db
                sqlStatementPlace_ID = "SELECT place_id FROM hoteldetails WHERE place_id = '{}';".format(SQL_Place_ID)
                cursor3.execute(sqlStatementPlace_ID)
                # get row from db
                row = cursor3.fetchone()

                # if there is no row
                if row == None:
                    # Google call for details
                    url2 = 'https://maps.googleapis.com/maps/api/place/details/json?'
                    params2 = {'placeid': SQL_Place_ID,
                               'key': APIKeys[0]}
                    # get response by url2
                    response2 = requests.get(url=url2, params=params2)
                    response_data2 = response2.json()
                    if response_data2['status'] == 'OVER_QUERY_LIMIT':
                        del APIKeys[0]
                    # if data retrieved correctly
                    if response_data2['status'] == 'OK':
                        result = response_data2.get("result", None)
                        place_id = result.get("place_id", None)
                        hotel_name = result.get("name", None)
                        address = result.get("formatted_address", None)
                        latitude = result['geometry']['location'].get("lat", None)
                        longitude = result['geometry']['location'].get("lng", None)
                        country = str(result.get("formatted_address", None)).split(", ")[-1]
                        print("\033[92m" + '+' + "\033[0m", hotel_name + ':', address, ',', '(', latitude, ',', longitude, ')')

                        cursor2.execute(sqlStatement, (
                            place_id, hotel_name, address, latitude, longitude, country))
                        connection2.commit()
                else:
                    pass

        time.sleep(2)
        # if there is the next page token, so work it out
        url1 = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        params1 = {'location': '%s,%s' % (latitude, longitude),
                   'radius': '%s' % args.radius,
                   'keyword': '%s' % args.word,
                   'key': APIKeys[0],
                   'pagetoken': page_token}
        # Get response by url1
        response1 = requests.get(url=url1, params=params1)
        response_data1 = response1.json()
        if response_data1['status'] == 'OVER_QUERY_LIMIT':
            del APIKeys[0]
        print('=== Getting next page from nearby search endpoint ===============>')

        if page_token == None:
            break

    # The end of current search
    print("\033[92m" + '{0}) Total Places saved: {1} near: {2}, {3} at {4}'.format(
        countdown_order, len(results), city_name, country_code,
        datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'), "\033[0m"))


def SQLQuery():

    # Connect to POstgreSQL
    connection = psycopg2.connect(Connection_Details)
    connection.autocommit = True
    cursor = connection.cursor()

    if args.country:
        sqlStatement = "WITH cte AS \
                          ( SELECT *, ROW_NUMBER() \
                            OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) \
                            AS rn, DENSE_RANK() \
                            OVER (ORDER BY city_name DESC) \
                            AS countdown_order \
                            FROM ip2location_db11 \
                            WHERE country_code = '{}' \
                          ) \
                             SELECT countdown_order, latitude, longitude, city_name, country_code \
                             FROM cte \
                             WHERE rn = 1 \
                             ORDER BY city_name".format(args.country)
    elif args.city:
        sqlStatement = "WITH cte AS \
                          ( SELECT *, ROW_NUMBER() \
                            OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) \
                            AS rn, DENSE_RANK() \
                            OVER (ORDER BY city_name DESC) \
                            AS countdown_order \
                            FROM ip2location_db11 \
                            WHERE city_name = '{}' \
                          ) \
                             SELECT countdown_order, latitude, longitude, city_name, country_code \
                             FROM cte \
                             WHERE rn = 1 \
                             ORDER BY city_name".format(args.city)
    if args.country and args.rownumber:
        sqlStatement = "WITH cte AS \
                          ( SELECT *, ROW_NUMBER() \
                            OVER (PARTITION BY latitude, longitude ORDER BY latitude, longitude) \
                            AS rn, DENSE_RANK() \
                            OVER (ORDER BY city_name desc) \
                            AS countdown_order \
                            FROM ip2location_db11 \
                            WHERE country_code = '{}' \
                          ) \
                             SELECT countdown_order, latitude, longitude, city_name, country_code \
                             FROM cte \
                             WHERE rn = 1 \
                             AND countdown_order <= '{}' \
                             ORDER BY city_name".format(args.country, args.rownumber)

    try:
        cursor.execute(sqlStatement)

        for countdown_order, latitude, longitude, city_name, country_code in cursor:
            if args.do == 'show':
                get_place_for_show(countdown_order, latitude, longitude, city_name, country_code)
            if args.do == 'save':
                get_place_for_save(countdown_order, latitude, longitude, city_name, country_code)
    finally:
        cursor.close()
        connection.close()


SQLQuery()
