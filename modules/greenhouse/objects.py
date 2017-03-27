#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.data.db import DBSharedProperty
from modules.greenhouse.models import SensorResultsDoc, \
                                      SoilConditions, AirInsideConditions, AirOutsideConditions, \
                                      LifecycleDoc, TimerDoc, ConditionDoc
from datetime import datetime


# class Condition(object):
#
#     ModelClass = ConditionDoc
#
#     type = DBSharedProperty('type')
#     auto = DBSharedProperty('auto')
#     min_value = DBSharedProperty('min_value')
#     max_value = DBSharedProperty('max_value')
#
#     def __init__(self, type=None, model=None):
#         assert type or model, 'type or model are required'
#         self.model = model or self.ModelClass.objects.get(type=type)
#
#     @classmethod
#     def create(cls, type, auto, min, max):
#         new_model = cls.ModelClass()
#         new_model.type = type
#         new_model.auto = auto
#         new_model.min_value = min
#         new_model.max_value = max
#         new_model.save()
#         return cls(model=new_model)
#
#     def update(self, auto, min, max):
#         if auto:
#             self.model.auto = auto
#         if min:
#             self.model.min = min
#         if max:
#             self.model.max = max
#         self.save()
#
#     def get_params(self):
#         model = self.ModelClass.objects.first()
#         return model.min_value, model.max_value
#
#     def save(self):
#         self.model.save()
#
#     def delete(self):
#         self.model.delete()
#
#
# class Action(object):
#
#     ModelClass = ActionDoc
#
#     type = DBSharedProperty('type')
#     start = DBSharedProperty('start')
#     stop = DBSharedProperty('stop')
#
#     def __init__(self, type=None, model=None):
#         assert type or model, 'type or model are required'
#         self.model = model or self.ModelClass.objects.get(type=type)
#
#     @classmethod
#     def create(cls, type, start, stop):
#         new_model = cls.ModelClass()
#         new_model.type = type
#         new_model.start = start
#         new_model.stop = stop
#         new_model.save()
#         return cls(model=new_model)
#
#     def update(self, start, stop):
#         if min:
#             self.model.start = start
#         if max:
#             self.model.stop = stop
#         self.save()
#
#     def get_params(self):
#         model = self.ModelClass.objects.first()
#         return model.start, model.stop
#
#     def save(self):
#         self.model.save()
#
#     def delete(self):
#         self.model.delete()


class Lifecycle(object):

    ModelClass = LifecycleDoc
    TimerModelClass = TimerDoc
    ConditionModelClass = ConditionDoc

    type = DBSharedProperty('type')
    by_time = DBSharedProperty('by_time')
    state = DBSharedProperty('state')
    timer = DBSharedProperty('timer')
    conditions = DBSharedProperty('conditions')
    last_event = DBSharedProperty('last_event')

    def __init__(self, type=None, model=None):
        assert type or model, 'type or model are required'
        self.model = model or self.ModelClass.objects.get(type=type)

    @classmethod
    def create(cls, **kwargs):
        new_model = cls.ModelClass()
        new_model = cls.populate(new_model, **kwargs)
        new_model.save()

    @classmethod
    def populate(cls, model, type, by_time, timer, conditions, last_event):
        model.type = type
        model.by_time = by_time
        if timer:
            model.timer = cls.TimerModelClass(start_date=timer.start_date, end_date=timer.end_date,
                                              start_time=timer.start_time, end_time=timer.end_time)
        if conditions:
            model.conditions = cls.ConditionModelClass(min_value=conditions.min_value,
                                                       max_value=conditions.max_value)
        return model

    def save(self):
        self.model.save()


class SensorResults(object):

    ModelClass = SensorResultsDoc
    SoilCondModelClass = SoilConditions
    AirInsideCondModelDoc = AirInsideConditions
    AirOutsideCondModelDoc = AirOutsideConditions

    def __init__(self, model=None):
        assert model, 'model is required'
        self.model = model

    @classmethod
    def create(cls, **kwargs):
        new_model = cls.ModelClass()
        new_model = cls.populate(new_model, **kwargs)
        new_model.save()

    @classmethod
    def populate(cls, model, DS18B20_air, DS18B20_soil, BH1750, DHT22, SoilMoisture):
        model.soil = cls.SoilCondModelClass(temperature=DS18B20_soil.temperature,
                                            moisture=SoilMoisture.moisture)
        model.air_outside = cls.AirOutsideCondModelDoc(temperature=DS18B20_air.temperature)
        model.air_inside = cls.AirInsideCondModelDoc(temperature=DHT22.temperature,
                                                     luminosity=BH1750.luminosity,
                                                     humidity=DHT22.humidity)
        return model
