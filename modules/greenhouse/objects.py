#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.data.db import DBSharedProperty
from modules.greenhouse.models import ConditionDoc, ActionDoc, SensorResultsDoc, \
                                      SoilConditions, AirInsideConditions, AirOutsideConditions
from datetime import datetime


class Condition(object):

    ModelClass = ConditionDoc

    type = DBSharedProperty('type')
    auto = DBSharedProperty('auto')
    min_value = DBSharedProperty('min_value')
    max_value = DBSharedProperty('max_value')

    def __init__(self, type=None, model=None):
        assert type or model, 'type or model are required'
        self.model = model or self.ModelClass.objects.get(type=type)

    @classmethod
    def create(cls, type, auto, min, max):
        new_model = cls.ModelClass()
        new_model.type = type
        new_model.auto = auto
        new_model.min_value = min
        new_model.max_value = max
        new_model.save()
        return cls(model=new_model)

    def update(self, auto, min, max):
        if auto:
            self.model.auto = auto
        if min:
            self.model.min = min
        if max:
            self.model.max = max
        self.save()

    def get_params(self):
        model = self.ModelClass.objects.first()
        return model.min_value, model.max_value

    def save(self):
        self.model.save()

    def delete(self):
        self.model.delete()


class Action(object):

    ModelClass = ActionDoc

    type = DBSharedProperty('type')
    start = DBSharedProperty('start')
    stop = DBSharedProperty('stop')

    def __init__(self, type=None, model=None):
        assert type or model, 'type or model are required'
        self.model = model or self.ModelClass.objects.get(type=type)

    @classmethod
    def create(cls, type, start, stop):
        new_model = cls.ModelClass()
        new_model.type = type
        new_model.start = start
        new_model.stop = stop
        new_model.save()
        return cls(model=new_model)

    def update(self, start, stop):
        if min:
            self.model.start = start
        if max:
            self.model.stop = stop
        self.save()

    def get_params(self):
        model = self.ModelClass.objects.first()
        return model.start, model.stop

    def save(self):
        self.model.save()

    def delete(self):
        self.model.delete()



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
    def populate(cls, model, ds18b20air, ds18b20soil, bh1750, dht22, soilmoisture):
        model.soil = cls.SoilCondModelClass(temperature=ds18b20soil.temperature,
                                            moisture=soilmoisture.moisture)
        model.air_outside = cls.AirOutsideCondModelDoc(temperature=ds18b20air.temperature)
        model.air_inside = cls.AirInsideCondModelDoc(temperature=dht22.temperature,
                                                     luminosity=bh1750.luminosity,
                                                     humidity=dht22.humidity)
        return model



if __name__ == '__main__':
    # Action.create('light', datetime(1970, 1, 1, 10, 00, 00), datetime(1970, 1, 1, 11, 00, 00))
    print Action('light').get_params()[0].hour # TODO: implement time comparison