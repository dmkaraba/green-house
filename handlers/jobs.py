#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.camera import Camera
from utils.sensors.reader import pull_data
from modules.greenhouse.objects import SensorResults


def insert_all_conditions():
    print '>>> insert_all_conditions <<<'
    answer = pull_data()
    SensorResults.create(ds18b20air=answer.DS18B20_air,
                         ds18b20soil=answer.DS18B20_soil,
                         bh1750=answer.BH1750,
                         dht22=answer.DHT22,
                         soilmoisture=answer.SoilMoisture)


def shoot_frame():
    Camera.shoot()


if __name__=='__main__':
    insert_all_conditions()
