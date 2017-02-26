#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.objects import Condition
from modules.const import SOIL_MOISTURE
from modules.greenhouse.sensors import SoilMoistureSensors
from modules.greenhouse.controllers import Pump


class SoilMoistureWatcher(object):

    condition = Condition(type=SOIL_MOISTURE)

    def __init__(self):
        self.min, self.max = self.condition.get_params()

    def hold(self):
        if self.condition.auto:
            value = SoilMoistureSensors().read().moisture

            if value <= self.min:
                Pump.pulse(3)
            elif value > self.max:
                # send warning email
                pass
        else:
            print 'This condition is not automated'


if __name__ == '__main__':
    # time.sleep(5)
    SoilMoistureWatcher().hold()
