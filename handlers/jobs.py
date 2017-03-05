#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.camera import Camera
from utils.sensors.reader import pull_data
from modules.greenhouse.objects import SensorResults


def insert_all_conditions():
    print '>>> insert_all_conditions <<<'
    answer = pull_data()
    measures = dict(answer)
    print measures
    del measures['rc']
    print measures
    SensorResults.create(**measures)


def shoot_frame():
    Camera.shoot()


if __name__=='__main__':
    insert_all_conditions()
