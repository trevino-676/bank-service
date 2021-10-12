from os import environ
from typing import Optional, List

import pymongo

from logger import logger


class AccountStatmentsService:
    def __init__(self):
        self.db = pymongo.MongoClient(environ.get("MONGO_URI")).robin_hood

    def get_movements(self, filters: dict) -> Optional[List]:
        try:
            movements = self.db[environ.get("ACCOUNT_STATMENT_COLLECTION")].find(filters)
            if movements.count() == 0:
                return None
            return list(movements)
        except Exception as e:
            logger.error(e)
            return None
