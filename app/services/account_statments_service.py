from os import environ

import pymongo

from logger import logger

db_route = environ.get("MONGO_URL")
client = pymongo.MongoClient(environ.get("MONOG_URI"))
db = client.robin_hood
collection = db[environ.get("ACCOUNT_STATMENT_COLLECTION")]


def get_account_statments(filters: dict) -> list:
    try:
        statments = collection.find(filters)
        return list(statments)
    except Exception as e:
        logger.error(e)
        return None
