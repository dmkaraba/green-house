#!/usr/bin/python
import datetime
from utils.sensors.reader import read_all
from utils.mongodb.connect import insert_one


def do_upload():
    data = read_all()
    record = {
        'conditions': data['result'],
        'date': datetime.datetime.now()
    }
    insert_one(record)


if __name__ == '__main__':
    do_upload()
