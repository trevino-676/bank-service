from os import environ

import pandas as pd
import numpy as np
import pymongo

from app.models import MISSING_MESSAGE
from logger import logger


class BBVAModel:
    def __init__(self, document):
        self.df = pd.read_excel(document)
        self.db = pymongo.MongoClient(environ.get("MONGO_URI")).robin_hood
        self.bbva_collection = self.db[environ.get("BBVA_COLLECTION")]
        self.account_statment_collection = self.db[
            environ.get("ACCOUNT_STATMENT_COLLECTION")
        ]
        self.mandatory_columns = [
            "Día",
            "Concepto / Referencia",
            "cargo",
            "Abono",
            "Saldo",
        ]

    def __verified_statments(self):
        is_valid = True
        missing_columns = []
        columns = list(self.df.columns)
        for column in columns:
            if column not in self.mandatory_columns:
                is_valid = False
                missing_columns.append(column)

        return is_valid, missing_columns

    def __clear_data(self):
        self.df = self.df.rename(
            columns={
                "Día": "fecha",
                "Concepto / Referencia": "concepto",
                "Abono": "abono",
                "Saldo": "saldo",
            }
        )
        self.df.cargo = self.df.cargo.replace(np.nan, 0)
        self.df.abono = self.df.abono.replace(np.nan, 0)
        self.df.saldo = self.df.saldo.replace(np.nan, 0)
        self.df.fecha = self.df.fecha.apply(lambda date: str(date))

    def __get_bbva_accounts_collection(self):
        return self.df.to_dict("records")

    def __map_account_statments_collection(self, item: dict):
        account = {}
        account["cliente"] = ""
        account["empresa"] = ""
        account["banco"] = "bbva"
        account["cuenta"] = ""
        account["descripcion"] = item["concepto"]
        account["referencia"] = ""
        account["fecha"] = item["fecha"]
        account["deposito"] = item["abono"]
        account["retiro"] = item["cargo"]
        account["saldo"] = item["saldo"]
        return account

    def __get_account_statments_collection(self):
        account_statments = self.df.to_dict("records")
        account_statments = list(
            map(self.__map_account_statments_collection, account_statments)
        )
        return account_statments

    def save_statments(self) -> bool:
        is_valid, missing_columns = self.__verified_statments()
        if not is_valid:
            raise Exception(MISSING_MESSAGE.format(str(missing_columns)))
        self.__clear_data()
        try:
            self.bbva_collection.insert_many(self.__get_bbva_accounts_collection())
            self.account_statment_collection.insert_many(
                self.__get_account_statments_collection()
            )
            return True
        except Exception as e:
            logger.error(e)
            return False
