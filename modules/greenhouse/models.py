#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules.data.db import DBDocument
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField,\
                        IntField, BooleanField, ListField, MapField, DynamicField, \
                        ObjectIdField, DateTimeField, FloatField, ReferenceField


### LIFECYCLE ###################################

class TimerDoc(EmbeddedDocument):
    start_date = DateTimeField()
    end_date = DateTimeField()
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)


class ConditionDoc(EmbeddedDocument):
    min_value = IntField(required=True)
    max_value = IntField()


class LifecycleDoc(DBDocument):

    meta = {'collection': 'lifecycle'}  # TODO: index - type

    type = StringField(required=True)
    by_time = BooleanField(required=True)
    active = BooleanField(default=True)
    state = BooleanField(default=False)
    timer = EmbeddedDocumentField(TimerDoc)
    conditions = EmbeddedDocumentField(ConditionDoc)
    last_event = DateTimeField()

### SENSOR RESULTS ##############################

class SoilConditions(EmbeddedDocument):
    temperature = FloatField()
    moisture = FloatField()


class AirOutsideConditions(EmbeddedDocument):
    temperature = FloatField()


class AirInsideConditions(EmbeddedDocument):
    temperature = FloatField()
    luminosity = FloatField()
    humidity = FloatField()


class SensorResultsDoc(DBDocument):

    meta = {'collection': 'measures'}

    soil = EmbeddedDocumentField(SoilConditions)
    air_outside = EmbeddedDocumentField(AirOutsideConditions)
    air_inside = EmbeddedDocumentField(AirInsideConditions)
    datetime = DateTimeField(default=datetime.datetime.now)
