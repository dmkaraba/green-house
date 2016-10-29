#!/usr/bin/python

import datetime
from utils.sensors.reader import read_all
from utils.mongodb.connect import insert_one
import utils.logger as logger


def inser_one_to_mongo():
    data = read_all()
    print data
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


if __name__=='__main__':
    print inser_one_to_mongo()
