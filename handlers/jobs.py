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
    print measures
    del measures['rc']
    print measures
    SensorResults.create(**measures)


def watch_for_lights():
    print '>>> perform lights scenario <<<'
    TimerWatchdog('light').watch()


def watch_for_fans():
    print '>>> perform fans scenario <<<'
    TimerWatchdog('fan').watch()


def watch_for_soilmoisture():
    print '>>> perform soilmoisture <<<'
    ConditinsWatchdog('soil_moisture', 'pump').watch()


# def shoot_frame():
#     print '>>> shoot frame <<<'
#     Camera.shoot()

