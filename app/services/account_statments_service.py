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

    def get_daily_group_movements(self, filters: dict) -> Optional[List]:
        try:
            movements = self.db[environ.get("ACCOUNT_STATMENT_COLLECTION")].aggregate(
                self.__get_aggregate_list(filters)
            )
            return list(movements)
        except Exception as e:
            logger.error(e)
            return None

    def __get_aggregate_list(self, filters: dict) -> list:
        return [
            {"$match": filters},
            {
                "$group": {
                    "_id": {"fecha": "$fecha", "banco": "$banco"},
                    "deposito": {"$sum": {"$toDouble": "$deposito"}},
                    "retiro": {"$sum": {"$toDouble": "$retiro"}},
                    "saldo": {"$last": "$saldo"},
                }
            },
            {"$sort": {"_id.fecha": 1}},
        ]
