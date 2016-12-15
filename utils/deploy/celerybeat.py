#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

from config import config

schedules = {}

for k, schedule in config.celerybeat['CELERYBEAT_SCHEDULE'].items():
    if 'timedelta' in schedule['schedule']:
        schedule['schedule'] = timedelta(**schedule['schedule']['timedelta'])
    elif 'crontab' in schedule['schedule']:
        schedule['schedule'] = crontab(**schedule['schedule']['crontab'])
    schedules.update({k: schedule})


config.celerybeat['CELERYBEAT_SCHEDULE'] = schedules


app = Celery()
app.conf.update(config.celerybeat)
