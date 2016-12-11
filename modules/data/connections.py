#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
from config.c import config


def get_mongo_connection():
    return pymongo.MongoClient(port=config.mongodb['port'])


mongo_connection = get_mongo_connection()
