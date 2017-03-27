#!/usr/bin/env python
# -*- coding: utf-8 -*-

from modules.greenhouse.camera import Camera
from modules.greenhouse.lifecycle import PerformerWatcher
from utils.sensors.reader import pull_data
from modules.greenhouse.objects import SensorResults


def insert_all_conditions():
    print '>>> insert all conditions <<<'
    answer = pull_data()
    measures = dict(answer)
    print measures
    del measures['rc']
    print measures
    SensorResults.create(**measures)


def perform_scenarios():
    print '>>> perform scenario <<<'
    PerformerWatcher('light').perform()


# def shoot_frame():
#     print '>>> shoot frame <<<'
#     Camera.shoot()

