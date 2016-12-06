#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import utils.logger as logger
from utils.sensors.reader import read_all
from utils.mongodb.connect import insert_one
from handlers.sensors import SoilMoistureSensors


# def shoot():
#     # task for frames shooting gona be here
#     print '>>> shoot <<<'
#     return 1
#
#
# def ones_job():
#     print '>>> ones <<<'
#     return 1


def insert_all_conditions():
    print '>>> insert_all_conditions <<<'
    data = read_all()
    if data['status'] == 'success':
        record = {
            'conditions': data['result'],
            'date': datetime.datetime.now()
        }
        try:
            insert_one(record)
            logger.info('Inserted condition data to mongoDB')
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


def soil_moisture_test():
    print '>>> soil_moisture_test <<<'
    s = SoilMoistureSensors()
    record = {
        'data':
        {
        '1': s.read_one(0)['result'],
        '2': s.read_one(1)['result'],
        '3': s.read_one(2)['result'],
        '4': s.read_one(3)['result']
        },
        'date': datetime.datetime.now()
    }
    try:
        insert_one(record, 'soil_test')
        logger.info('Inserted condition data to mongoDB')
        return {'status': 'success'}
    except:
        logger.error('Fail to insert condition data to mongoDB')
        return {'status': 'fail', 'msg': 'Fail inserting data'}
