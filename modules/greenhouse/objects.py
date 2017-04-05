#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.data.db import DBSharedProperty
from modules.greenhouse.models import SensorResultsDoc, \
                                      SoilConditions, SoilMoistureConditions,\
                                      AirInsideConditions, AirOutsideConditions, \
                                      LifecycleDoc, TimerDoc, ConditionDoc


class Lifecycle(object):

    ModelClass = LifecycleDoc
    TimerModelClass = TimerDoc
    ConditionModelClass = ConditionDoc

    type = DBSharedProperty('type')
    by_time = DBSharedProperty('by_time')
    state = DBSharedProperty('state')
    active = DBSharedProperty('active')
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
    SoilMoistureModelClass = SoilMoistureConditions
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
    def populate(cls, model, DS18B20_air, DS18B20_soil, BH1750, DHT22,
                 Soil_moisture_a, Soil_moisture_b, Soil_moisture_c, Soil_moisture_d, **kwargs):
        soil_moisture = cls.SoilMoistureModelClass(a=Soil_moisture_a.moisture,
                                                   b=Soil_moisture_b.moisture,
                                                   c=Soil_moisture_c.moisture,
                                                   d=Soil_moisture_d.moisture)
        model.soil = cls.SoilCondModelClass(temperature=DS18B20_soil.temperature,
                                            moisture=soil_moisture)
        model.air_outside = cls.AirOutsideCondModelDoc(temperature=DS18B20_air.temperature)
        model.air_inside = cls.AirInsideCondModelDoc(temperature=DHT22.temperature,
                                                     luminosity=BH1750.luminosity,
                                                     humidity=DHT22.humidity)
        return model
