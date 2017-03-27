#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules import const
from modules.greenhouse.objects import Lifecycle
from modules.greenhouse.sensors import SoilMoistureSensors
from modules.greenhouse.controllers import Pump, Light
from utils.mixins import DateComparison, TimeComparison
from modules.const import PERFORMERS


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


# class SoilMoistureWatcher(object):
#
#     condition = Condition(type=const.SOIL_MOISTURE)
#
#     def __init__(self):
#         self.min, self.max = self.condition.get_params()
#
#     def hold(self):
#         if self.condition.auto:
#             value = SoilMoistureSensors().read().moisture
#
#             if value <= self.min:
#                 Pump.pulse(3)
#             elif value > self.max:
#                 # send warning email
#                 pass
#         else:
#             print 'This condition is not automated'


class PerformerWatcher(object):

    def __init__(self, performer):
        self.performer = PERFORMERS[performer]
        self.lifecycle_obj = Lifecycle(type=performer)
        self.timer = Lifecycle(type=performer).timer
        self.conditions = Lifecycle(type=performer).conditions
        self.last_event = Lifecycle(type=performer).last_event

    def satisfy_time(self):
        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)
        timer_start_time = TimeComparison(self.timer.start_time.hour, self.timer.start_time.minute)
        timer_end_time = TimeComparison(self.timer.end_time.hour, self.timer.end_time.minute)
        return timer_end_time >= time >= timer_start_time

    def satisfy_date(self):
        if self.timer.start_date and self.timer.end_date:
            timer_start_date = DateComparison(self.timer.start_date.year, self.timer.start_date.month, self.timer.start_date.day)
            timer_end_date = DateComparison(self.timer.end_date.year, self.timer.end_date.month, self.timer.end_date.day)
            return timer_end_date >= DateComparison.today() >= timer_start_date
        else:
            return True

    def satisfied_last_event(self):
        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)
        if self.last_event:
            last_event_time = TimeComparison(self.last_event.hour, self.last_event.minute)
            return time <= last_event_time
        else:
            return True

    def perform(self):
        if self.satisfy_date() and self.satisfy_time() and self.satisfied_last_event():
            if not self.lifecycle_obj.state:
                self.performer.set_up()
                self.performer.on()
                self.lifecycle_obj.state = True
                self.lifecycle_obj.last_event = datetime.datetime.now()
                self.lifecycle_obj.save()
        elif not self.satisfy_time() or not self.satisfy_date():
            if self.lifecycle_obj.state:
                self.performer.set_up()
                self.performer.off()
                self.lifecycle_obj.state = False
                self.lifecycle_obj.last_event = datetime.datetime.now()
                self.lifecycle_obj.save()
