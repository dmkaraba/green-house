#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery
from celery.schedules import crontab
from config.c import config


# app = Celery()
# app.conf.beat_schedule = {
#     'all-to-db-10min': {
#         'task': 'handlers.tasks.insert_all_conditions',
#         'schedule': crontab(minute='*/2')
#     },
#     'soil-to-db': {
#         'task': 'handlers.tasks.soil_moisture_test',
#         'schedule': crontab(minute='*/1')
#     }
# }

print config.celerybeat

app = Celery()
app.conf.update(config.celerybeat)