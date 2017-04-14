#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.controllers import PumpA, PumpB, Light, Fan
from modules.greenhouse.sensors import BH1750, DHT22, DS18B20_Air, DS18B20_Soil,\
                                       SoilMoistureA, SoilMoistureB


SENSORS = {
    'soil_moisture_a': SoilMoistureA,  # TODO: add sensors
    'soil_moisture_b': SoilMoistureB,
}

PERFORMERS = {
    'light': Light,
    'pump_a': PumpA,
    'pump_b': PumpB,
    'fan': Fan
}
