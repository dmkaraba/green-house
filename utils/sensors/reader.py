#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.sensor_answers import AllSensorsAnswer
from modules.greenhouse.sensors import DS18B20_Air, DS18B20_Soil, \
                                       BH1750, DHT22, SoilMoistureSensors


def pull_data():
    results = dict()
    results['DS18B20_air'] = DS18B20_Air().read()
    results['DS18B20_soil'] = DS18B20_Soil().read()
    results['BH1750'] = BH1750().read()
    results['DHT22'] = DHT22().read()
    results['SoilMoisture'] = SoilMoistureSensors().read()
    return AllSensorsAnswer(results)


if __name__=='__main__':
    print pull_data()
