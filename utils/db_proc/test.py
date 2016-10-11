from pymongo import MongoClient


connection = MongoClient('localhost', 27017)

db = connection.new_db
data = db.data

items = data.find()
