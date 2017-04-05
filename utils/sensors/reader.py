#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.sensor_answers import AllSensorsResult
from modules.greenhouse.sensors import DS18B20_Air, DS18B20_Soil, \
                                       BH1750, DHT22, SoilMoistureSensors


def pull_data():
    sm = SoilMoistureSensors()
    res = AllSensorsResult({
        'DS18B20_air': DS18B20_Air().read(),
        'DS18B20_soil': DS18B20_Soil().read(),
        'BH1750': BH1750().read(),
        'DHT22': DHT22().read(),
        'Soil_moisture_a': sm.read_one(0),
        'Soil_moisture_b': sm.read_one(1),
        'Soil_moisture_c': sm.read_one(2),
        'Soil_moisture_d': sm.read_one(3)
    })
    return res


if __name__=='__main__':
    print pull_data()
