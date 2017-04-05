#!/usr/bin/env python
# -*- coding: utf-8 -*-

from schematics.models import Model
from schematics.types.compound import ModelType
from schematics import types


class BaseSensorResult(Model):
    rc = types.IntType(default=0)


class BH1750Result(BaseSensorResult):
    luminosity = types.FloatType()


class DHT22Result(BaseSensorResult):
    temperature = types.FloatType()
    humidity = types.FloatType()


class DS18B20Result(BaseSensorResult):
    temperature = types.FloatType()


class SoilMoistureResult(BaseSensorResult):
    moisture = types.FloatType()


class AllSensorsResult(BaseSensorResult):
    BH1750 = ModelType(BH1750Result)
    DHT22 = ModelType(DHT22Result)
    DS18B20_air = ModelType(DS18B20Result)
    DS18B20_soil = ModelType(DS18B20Result)
    Soil_moisture_a = ModelType(SoilMoistureResult)
    Soil_moisture_b = ModelType(SoilMoistureResult)
    Soil_moisture_c = ModelType(SoilMoistureResult)
    Soil_moisture_d = ModelType(SoilMoistureResult)
