import pymongo
from pymongo import MongoClient
import logging

# initialize db
MDB_URL = "mongodb+srv://readonly:readonly@covid-19.hip2i.mongodb.net/covid19"
client = MongoClient(MDB_URL)
db = client.get_database("covid19")
global_stat = db.get_collection("global")
metadata = db.get_collection("metadata")


def fetch_cases(last_date, country='ALL'):
    total_confirmed = 0
    total_deaths = 0
    total_recovered = 0

    if country == 'ALL':
        results = global_stat.find({"date": last_date})
    else:
        results = global_stat.find({"date": last_date , "country":country})

    for result in results:
        try:
            total_confirmed += result['confirmed']
        except Exception as e:
            logging.warning(e)
        try:
            total_deaths += result['deaths']
        except Exception as e:
            logging.warning(e)

        try:
            total_recovered += result["recovered"]

        except Exception as e:
            logging.warning(e)

    return total_confirmed , total_deaths, total_recovered

def fetch_cases_date_diff(current_date,before_date):
    t_confirmed , t_deaths , _ = fetch_cases(current_date)
    y_confirmed , y_deaths , _ = fetch_cases(before_date)
    inc_confirmed = t_confirmed - y_confirmed
    inc_deaths = t_deaths - y_deaths
    return inc_confirmed, inc_deaths


def get_latest_metadata():
    meta = metadata.find_one()
    return meta

def find_top(lastdate,top=10):
    # Requires the PyMongo package.
    # https://api.mongodb.com/python/current
    result = global_stat.aggregate([
            {
                '$match': {
                    'date': lastdate
                }
            }, {
                '$group': {
                    '_id': '$country',
                    'country': {"$first": "$country"},
                    'confirmed': {
                        '$sum': '$confirmed'
                    },
                    'deaths': {
                        '$sum': '$deaths'
                    },
                    'recovered': {
                        '$sum': '$recovered'
                    }
                }
            }, {
                '$sort': {
                    'confirmed': -1
                }
            }, {
                '$limit': top
            }
        ])

    return result
