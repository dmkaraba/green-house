#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.controllers import Pump, Light, Fan
from modules.greenhouse.sensors import BH1750, DHT22, DS18B20_Air, \
                                       DS18B20_Soil, SoilMoistureSensors


SOIL_MOISTURE = 'soil_moisture'

SENSORS = {
    'soil_moisture': SoilMoistureSensors,
}

PERFORMERS = {
    'light': Light,
    'pump': Pump,
    'fan': Fan
}