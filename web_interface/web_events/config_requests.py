#!/usr/bin/env python
# -*- coding: utf-8 -*-

from schematics import types
from schematics.models import Model
from schematics.types.compound import ModelType


### LIFECYCLE ###################################

class Timer(Model):
    start_date = types.DateTimeType()
    end_date = types.DateTimeType()
    start_time = types.DateTimeType(required=True)
    end_time = types.DateTimeType(required=True)


class Conditions(Model):
    min_value = types.IntType(required=True)
    max_value = types.IntType()


class CreateLifecycle(Model):
    type = types.StringType(required=True)
    by_time = types.BooleanType(required=True)
    timer = ModelType(Timer)
    conditions = ModelType(Conditions)
    last_event = types.DateTimeType()
