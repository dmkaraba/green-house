from pymongo import MongoClient
from handlers.sensors import DS18B20, BH1750, DHT22
import datetime
import time


def measure_all():
    soil_temp = DS18B20('soil').read()
    air_outside_temp = DS18B20('air').read()
    luminosity = BH1750().read()
    air_inside = DHT22().read()
    return soil_temp, air_outside_temp, luminosity, air_inside


def push_to_db():
    connection = MongoClient('localhost', 27017)

    db = connection.new_db
    coll = db.data

    r = {
        'soil_temperature': int(results[0]['result']*1000),
        'air_out_temperature': int(results[1]['result']*1000),
        'luminosity': int(results[2]['result']*1000),
        'air_inside': {'temperature': int(results[3]['result']['temperature']*1000),
                       'humidity': int(results[3]['result']['humidity']*1000)},
        'date': datetime.datetime.now()
        }

    a = coll.insert_one(r)
    print a.inserted_id

    connection.close()

if __name__ == '__main__':
    while True:
        results = measure_all()
        push_to_db()
        time.sleep(600)
