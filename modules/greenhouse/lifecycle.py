#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules.greenhouse.objects import Condition, Action
from modules.const import SOIL_MOISTURE, LIGHT
from modules.greenhouse.sensors import SoilMoistureSensors
from modules.greenhouse.controllers import Pump
from utils.mixins import DateComparison, TimeComparison


def compare_logic(a, b, op):
    if op == 'eq':
        return a == b
    elif op == 'gt':
        return a > b
    elif op == 'lt':
        return a < b
    elif op == 'gte':
        return a >= b
    elif op == 'lte':
        return a <= b
    else:
        raise Exception('Unsupported operation %s' % op)


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


class LightsWatcher(object):

    action = Action(type=LIGHT)

    def __init__(self):
        self.start, self.stop = self.action.get_params()

    def satisfy_timer(self, timer): # TODO: rebuild shturmans timer object. Timer is condition.params
        today = DateComparison.today()
        weekday = today.weekday()

        now = datetime.datetime.now()
        time = TimeComparison(now.hour, now.minute)

        timer_start_date = timer.get('start_date').date() if timer.get('start_date') else ''
        timer_end_date = timer.get('end_date').date() if timer.get('end_date') else ''
        timer_start_time = timer.get('start_time').time() if timer.get('start_time') else ''
        timer_end_time = timer.get('end_time').time() if timer.get('end_time') else ''
        timer_weekdays = timer.get('weekdays')

        satisfied_time_date = False
        satisfied_weekdays = True

        # date and time checking
        if timer_start_time and timer_end_time:
            if timer_start_date and timer_end_date:
                # date and time comporation
                if timer_end_date > today > timer_start_date:
                    satisfied_time_date = True
                elif timer_end_date == today and today == timer_start_date:
                    # time only check
                    if timer_end_time >= time >= timer_start_time:
                        satisfied_time_date = True
                    else:
                        satisfied_time_date = False
                elif today == timer_end_date and time <= timer_end_time:
                    satisfied_time_date = True
                elif today == timer_start_date and time >= timer_start_time:
                    satisfied_time_date = True
            else:
                # just time comporation
                if timer_end_time >= time >= timer_start_time:
                    satisfied_time_date = True
                else:
                    satisfied_time_date = False

        # weekdays checking
        if timer_weekdays and weekday not in timer_weekdays:
            satisfied_weekdays = False

        return satisfied_time_date and satisfied_weekdays

if __name__ == '__main__':
    # time.sleep(5)
    SoilMoistureWatcher().hold()
