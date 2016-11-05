#!/usr/bin/python

from __future__ import absolute_import, unicode_literals
from .celery import app


# @app.task
def shoot():
    # task for frames shooting gona be here
    return 1