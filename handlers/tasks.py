#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import config
from utils.deploy.celerybeat import app as celerybeat_app
from utils.deploy.celeryd import app as celeryd_app


@celerybeat_app.task(ignore_result=True, queue='main')
def insert_all_conditions():
    from handlers.jobs import insert_all_conditions
    insert_all_conditions()

@celerybeat_app.task(ignore_result=True, queue='main')
def soil_moisture_test():
    from handlers.jobs import soil_moisture_test
    soil_moisture_test()

@celerybeat_app.task(ignore_result=True, queue='main')
def shoot_frame():
    from handlers.jobs import shoot_frame
    shoot_frame()

@celeryd_app.task(ignore_result=True, queue='mqtt')
def fans():
    from modules.mqtt_interaction.base import FansMQTTClass
    FansMQTTClass().sub(config.mqtt_topics_sub['fans'])

@celeryd_app.task(ignore_result=True, queue='mqtt')
def lights():
    from modules.mqtt_interaction.base import LightMQTTClass
    LightMQTTClass().sub(config.mqtt_topics_sub['lights'])

@celeryd_app.task(ignore_result=True, queue='mqtt')
def pumps():
    from modules.mqtt_interaction.base import PumpsMQTTClass
    PumpsMQTTClass().sub(config.mqtt_topics_sub['pumps'])

@celeryd_app.task(ignore_result=True, queue='mqtt')
def sensors():
    from modules.mqtt_interaction.handlers import SensorsMQTTDmn
    SensorsMQTTDmn().run()


fans.apply_async()
lights.apply_async()
pumps.apply_async()
sensors.apply_async()

# TODO: add lights on/off task

