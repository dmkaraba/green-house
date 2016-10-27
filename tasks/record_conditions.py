#!/usr/bin/python
import datetime
from utils.sensors.reader import read_all
from utils.mongodb.connect import insert_one

# works from greenhouse
# doesnot work from dev

def do_upload():
    data = read_all()
    print data
    record = {
        'conditions': data['result'],
        'date': datetime.datetime.now()
    }
    # insert_one(record)
    print 'OK'
do_upload()