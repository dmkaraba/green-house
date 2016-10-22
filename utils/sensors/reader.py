#!/usr/bin/python
from handlers.sensors import DS18B20, BH1750, DHT22
import datetime


def read_all():
    attempts = 3
    while attempts:
        try:
            soil_temp = DS18B20('soil').read()
            air_outside_temp = DS18B20('air').read()
            luminosity = BH1750().read()
            air_inside = DHT22().read()
            data = {
                'soil_temperature': soil_temp['result'],
                'air_out_temperature': air_outside_temp['result'],
                'luminosity': luminosity['result'],
                'air_inside': {'temperature': air_inside['result']['temperature'],
                               'humidity': air_inside['result']['humidity']}
            }
            result = {'status': 'success', 'result': data}
            return result
        except:
            attempts = attempts - 1
    return {'status': 'fail', 'msg': 'Fail to read'}


if __name__=='__main__':
    read_all()
