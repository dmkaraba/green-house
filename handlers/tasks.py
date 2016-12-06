#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.deploy.celeryd import app as celeryd_app
from utils.deploy.celerybeat import app as celerybeat_app


@celerybeat_app.task
def insert_all_conditions():
    from handlers.jobs import insert_all_conditions
    insert_all_conditions()

@celerybeat_app.task
def soil_moisture_test():
    from handlers.jobs import soil_moisture_test
    soil_moisture_test()

# @celeryd_app.task(ignore_result=True, queue='qqq')
# def just_print():
#     from handlers.jobs import ones_job
#     ones_job()
#
# @celerybeat_app.task
# def shooting():
#     from handlers.jobs import shoot
#     shoot()
