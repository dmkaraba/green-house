#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules import const
from modules.greenhouse.objects import Lifecycle
from modules.greenhouse.sensors import SoilMoistureSensors
from modules.greenhouse.controllers import Pump, Light
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


class LightsWatcher(object):

    lifecycle_obj = Lifecycle(type=const.LIGHT)
    performer = Light

    def __init__(self):
        self.timer = self.lifecycle_obj.timer
        self.conditions = self.lifecycle_obj.conditions

    @classmethod
    def satisfy_timer(cls):

        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)

        timer = cls.lifecycle_obj.timer
        timer_start_time = TimeComparison(timer.start_time.hour, timer.start_time.minute)
        timer_end_time = TimeComparison(timer.end_time.hour, timer.end_time.minute)

        if timer.start_date and timer.end_date:
            today = DateComparison.today()
            timer_start_date = DateComparison(timer.start_date.year, timer.start_date.month, timer.start_date.day)
            timer_end_date = DateComparison(timer.end_date.year, timer.end_date.month, timer.end_date.day)
        else:
            timer_start_date = timer_end_date = today = ''

        satisfied_time_date = False

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

        return satisfied_time_date

    @classmethod
    def satisfy_schedule(cls):

        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)

        timer = cls.lifecycle_obj.timer
        timer_start_time = TimeComparison(timer.start_time.hour, timer.start_time.minute)

        satisfied_last_event = False

        if cls.lifecycle_obj.last_event:
            last_event_time = TimeComparison(cls.lifecycle_obj.last_event.hour, cls.lifecycle_obj.last_event.minute)
            if time <= last_event_time:
                satisfied_last_event = True
        else:
            if time >= timer_start_time:
                satisfied_last_event = True

        return cls.satisfy_timer() and satisfied_last_event

    @classmethod
    def satisfy_time(cls):

        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)

        timer = cls.lifecycle_obj.timer
        timer_start_time = TimeComparison(timer.start_time.hour, timer.start_time.minute)
        timer_end_time = TimeComparison(timer.end_time.hour, timer.end_time.minute)

        return timer_end_time >= time >= timer_start_time

    @classmethod
    def satisfy_date(cls):

        timer = cls.lifecycle_obj.timer

        if timer.start_date and timer.end_date:
            timer_start_date = DateComparison(timer.start_date.year, timer.start_date.month, timer.start_date.day)
            timer_end_date = DateComparison(timer.end_date.year, timer.end_date.month, timer.end_date.day)
            return timer_end_date >= DateComparison.today() >= timer_start_date
        else:
            return True

    @classmethod
    def satisfied_last_event(cls):

        time = TimeComparison(datetime.datetime.now().hour, datetime.datetime.now().minute)

        if cls.lifecycle_obj.last_event:
            last_event_time = TimeComparison(cls.lifecycle_obj.last_event.hour, cls.lifecycle_obj.last_event.minute)
            return not time > last_event_time
        return True

    @classmethod
    def perform(cls):
        if cls.satisfy_date() and cls.satisfy_time() and cls.satisfied_last_event():
            if not cls.lifecycle_obj.state:
                cls.performer.set_up()
                cls.performer.on()
                cls.lifecycle_obj.state = True
                cls.lifecycle_obj.last_event = datetime.datetime.utcnow
                cls.lifecycle_obj.save()
                print 'ON'
        elif not cls.satisfy_time() or not cls.satisfy_date():
            if cls.lifecycle_obj.state:
                cls.performer.set_up()
                cls.performer.off()
                cls.lifecycle_obj.state = False
                cls.lifecycle_obj.last_event = datetime.datetime.utcnow
                cls.lifecycle_obj.save()
                print 'OFF'


if __name__ == '__main__':
    LightsWatcher.perform()
