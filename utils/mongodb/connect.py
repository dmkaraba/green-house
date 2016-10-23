from config import mongodb_conf
from pymongo import MongoClient


def insert_one(data):

    DB_NANE = mongodb_conf['db_name']
    CONDITIONS_COLLECTION = mongodb_conf['conditions_coll']

    connection = MongoClient('localhost', 27017)
    db = connection[DB_NANE]
    coll = db[CONDITIONS_COLLECTION]

    result = coll.insert_one(data)
    # print result.inserted_id

    connection.close()
