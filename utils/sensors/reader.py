#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.sensors import DS18B20_Air, DS18B20_Soil, \
                                       BH1750, DHT22, SoilMoistureSensors
from modules.greenhouse.sensor_answers import AllSensorsAnswer


def pull_data():
    attempts = 3
    while attempts:
        try:
            AllSensorsAnswer.DS18B20_air = DS18B20_Air().read()
            AllSensorsAnswer.DS18B20_soil = DS18B20_Soil().read()
            AllSensorsAnswer.BH1750 = BH1750().read()
            AllSensorsAnswer.DHT22 = DHT22().read()
            AllSensorsAnswer.SoilMoisture = SoilMoistureSensors().read()
            return AllSensorsAnswer
        except:
            attempts = attempts - 1
    AllSensorsAnswer.rc = 60
    return AllSensorsAnswer


def read_all():
    raw_data = pull_data()
    if raw_data:
        soil_temperature = raw_data[0].get('result', None)
        air_out_temperature = raw_data[1].get('result', None)
        luminosity = raw_data[2].get('result', None)
        air_temperature_inside = raw_data[3].get('result', dict()).get('temperature', None)
        air_humudity_inside = raw_data[3].get('result', dict()).get('humidity', None)
        soil_moisture = raw_data[4].get('result', None)
        data = {
            'soil': {
                'temperature': soil_temperature,
                'moisture': soil_moisture
            },
            'air_outside': {
                'temperature': air_out_temperature
                },
            'air_inside': {
                'temperature': air_temperature_inside,
                'humidity': air_humudity_inside,
                'luminosity': luminosity
            }
        }
        return {'status': 'success', 'result': data}
    else:
        return {'status': 'fail', 'msg': 'fail to read data'}


if __name__=='__main__':
    print read_all()
