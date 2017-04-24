#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from modules.greenhouse.objects import Lifecycle
from web_interface.web_events.config_requests import CreateLifecycle, Timer, Conditions
from datetime import datetime
from handlers.jobs import watch_for_soilmoisture_a, watch_for_fans, watch_for_lights
from modules.greenhouse.controllers import PumpA, PumpB
from modules.greenhouse.sensors import SoilMoistureSensors


T = Timer({
    'start_time': datetime(2017, 1, 1, 7, 0, 0),
    'end_time': datetime(2017, 1, 1, 20, 0, 0),
    'start_date': datetime(2017, 3, 3, 0, 0, 0),
    'end_date': datetime(2017, 3, 15, 0, 0, 0),
})
C = Conditions({'min_value': 30, 'max_value': 70})

data = {
    'by_time': False,
    'type': 'soil_moisture_b',
    # 'timer': T,
    'conditions': C
    }


def test_soilMo():
    print SoilMoistureSensors().read_all_raw()
    print SoilMoistureSensors().read()


if __name__ == '__main__':
    test_soilMo()
    # lc = CreateLifecycle(data)
    # Lifecycle.create(**lc)

    # watch_for_fans()
    # watch_for_lights()
    # watch_for_soilmoisture_a()
    # watch_for_soilmoisture_b()