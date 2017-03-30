#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules.greenhouse.objects import Lifecycle
from utils.mixins import DateComparison, TimeComparison
from modules.const import PERFORMERS, SENSORS


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


class BaseWatchdog(object):

    def __init__(self):
        self.sensor = None
        self.performer = None
        self.lifecycle_obj = None
        self.timer = None
        self.last_event = None

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
        date = DateComparison(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        if self.last_event:
            last_event_time = TimeComparison(self.last_event.hour, self.last_event.minute)
            last_event_date = DateComparison(self.last_event.year, self.last_event.month, self.last_event.day)
            if date > last_event_date:
                return True
            else:
                return time <= last_event_time
        else:
            return True

    def watch(self):
        print '>>> Timer watch'
        print self.satisfy_date(), self.satisfy_time(), self.satisfied_last_event()
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


class TimerWatchdog(BaseWatchdog):

    def __init__(self, performer):
        super(TimerWatchdog, self).__init__()
        self.performer = PERFORMERS[performer]
        self.lifecycle_obj = Lifecycle(type=performer)
        self.timer = Lifecycle(type=performer).timer
        self.last_event = Lifecycle(type=performer).last_event


class ConditinsWatchdog(BaseWatchdog):

    def __init__(self, condition, performer):  # soil_moisture pump
        super(ConditinsWatchdog, self).__init__()
        self.sensor = SENSORS[condition]()
        self.performer = PERFORMERS[performer]
        self.lifecycle_obj = Lifecycle(type=condition)
        self.conditions = Lifecycle(type=condition).conditions
        self.last_event = Lifecycle(type=condition).last_event

    def satisfy_conditions(self):
        value = self.sensor.read().moisture
        goal = self.conditions
        print goal.min_value, value
        # return value < goal.min_value  # TODO: we need 50% moisture (for example)
        return False

    def satisfied_last_event(self, delta_minutes=30):
        time_object_to_compare = datetime.datetime.now() - datetime.timedelta(minutes=delta_minutes)
        time_to_compare = TimeComparison(time_object_to_compare.hour, time_object_to_compare.minute)
        if self.last_event:
            last_event_time = TimeComparison(self.last_event.hour, self.last_event.minute)
            return time_to_compare > last_event_time
        else:
            return True

    def watch(self):
        print '>>> Condition watch'
        print self.satisfy_conditions(), self.satisfied_last_event()
        if self.satisfy_conditions() and self.satisfied_last_event():
            self.performer.pulse(3)
            self.lifecycle_obj.last_event = datetime.datetime.now()
            self.lifecycle_obj.save()
