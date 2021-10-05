from os import environ

import pymongo


db_client = pymongo.MongoClient(environ.get("MONGO_URI"))
db = db_client.robin_hood

# Message constants
MISSING_MESSAGE= "El archivo es incorrecto. Faltan las siguientes columnas: {}"
