#!/usr/bin/env python
# -*- coding: utf-8 -*-

from schematics.models import Model
from schematics.types.compound import ModelType
from schematics import types


class BaseSensorAnswer(Model):
    rc = types.IntType(default=0)


class BH1750Result(BaseSensorAnswer):
    luminosity = types.FloatType()


class DHT22Result(BaseSensorAnswer):
    temperature = types.FloatType()
    humidity = types.FloatType()


class DS18B20Result(BaseSensorAnswer):
    temperature = types.FloatType()


class SoilMoistureResult(BaseSensorAnswer):
    moisture = types.FloatType()


class AllSensorsAnswer(BaseSensorAnswer):
    BH1750 = ModelType(BH1750Result)
    DHT22 = ModelType(DHT22Result)
    DS18B20_air = ModelType(DS18B20Result)
    DS18B20_soil = ModelType(DS18B20Result)
    SoilMoisture = ModelType(SoilMoistureResult)
