#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery
from config.c import config


# app = Celery('main_app',
#              broker='amqp://guest@localhost//',
#              include=['handlers.tasks'])

# app.conf.timezone = 'Europe/Minsk'

print config.celeryd

app = Celery()
app.conf.update(config.celeryd)

