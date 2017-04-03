#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.camera import Camera
from modules.greenhouse.lifecycle import TimerWatchdog, ConditinsWatchdog
from utils.sensors.reader import pull_data
from modules.greenhouse.objects import SensorResults


def insert_all_conditions():
    print '>>> insert all conditions <<<'
    answer = pull_data()
    measures = dict(answer)
    del measures['rc']
    SensorResults.create(**measures)


def watch_for_lights():
    print '>>> perform lights scenario <<<'
    TimerWatchdog('light').watch()


def watch_for_fans():
    print '>>> perform fans scenario <<<'
    TimerWatchdog('fan').watch()


def watch_for_soilmoisture_a():
    print '>>> perform soilmoisture A <<<'
    ConditinsWatchdog('soil_moisture_a', 'pump_a').watch()


def watch_for_soilmoisture_b():
    print '>>> perform soilmoisture B <<<'
    ConditinsWatchdog('soil_moisture_b', 'pump_b').watch()


# def shoot_frame():
#     print '>>> shoot frame <<<'
#     Camera.shoot()

