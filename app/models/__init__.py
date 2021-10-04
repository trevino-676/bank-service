from os import environ

import pymongo


db_client = pymongo.MongoClient(environ.get("MONGO_URI"))
db = db_client.robin_hood
