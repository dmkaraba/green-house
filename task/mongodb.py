#!/usr/bin/python

from __future__ import absolute_import, unicode_literals
import datetime
from utils.sensors.reader import read_all
from utils.mongodb.connect import insert_one
import utils.logger as logger
from .celery import app


@app.task
def insert_all_conditions():
    data = read_all()
    if data['status'] == 'success':
        record = {
            'conditions': data['result'],
            'date': datetime.datetime.now()
        }
        try:
            # insert_one(record)
            logger.info('Inserted condition data to mongoDB')
            print record
            return {'status': 'success'}
        except:
            logger.error('Fail to insert condition data to mongoDB')
            return {'status': 'fail', 'msg': 'Fail inserting data'}
    else:
        logger.error('Reading data status {}'.format(data['status']))
        answer = dict()
        answer['status'] = 'fail'
        answer['msg'] = data['msg']
        return answer
