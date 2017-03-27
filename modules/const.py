#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.controllers import Pump, Light, Fan


SOIL_MOISTURE = 'soil_moisture'

SENSORS = {

}

PERFORMERS = {
    'light': Light,
    'pump': Pump,
    'fan': Fan
}