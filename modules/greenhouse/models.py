#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from modules.data.db import DBDocument
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, StringField,\
                        IntField, BooleanField, ListField, MapField, DynamicField, \
                        ObjectIdField, DateTimeField, FloatField, ReferenceField


class ConditionDoc(DBDocument):

    meta = {'collection': 'lifecycle.conditions'}

    type = StringField(required=True)
    auto = BooleanField(required=True)
    min_value = FloatField()
    max_value = FloatField()


class ActionDoc(DBDocument):

    meta = {'collection': 'lifecycle.actions'}

    type = StringField(required=True)
    start = DateTimeField()
    stop = DateTimeField()


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

    meta = {'collection': 'conditions'}

    soil = EmbeddedDocumentField(SoilConditions)
    air_outside = EmbeddedDocumentField(AirOutsideConditions)
    air_inside = EmbeddedDocumentField(AirInsideConditions)
    datetime = DateTimeField(default=datetime.datetime.utcnow)
