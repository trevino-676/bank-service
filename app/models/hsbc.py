from os import environ

import pandas as pd
import numpy as np
import pymongo

from logger import logger
from app.models import MISSING_MESSAGE


class HSBCModel:
    def __init__(self, document):
        self.df = pd.read_excel(document)
        self.__client = pymongo.MongoClient(environ.get("MONGO_URI"))
        self.__db = self.__client.robin_hood
        self.collection = self.__db[environ.get("HSBC_COLLECTION")]
        self.statments_collection = self.__db[environ.get("ACCOUNT_STATMENT_COLLECTION")]
        self.mandatory_columns = [
            'Nombre de la cuenta',
            'Número de cuenta',
            'Nombre del banco',
            'Divisa',
            'País',
            'Estatus de la cuenta',
            'Tipo de cuenta',
            'Referencia del Banco',
            'Narrativa adicional',
            'Referencia del cliente',
            'Tipo TRN',
            'Importe del abono',
            'Importe del cargo',
            'Saldo',
            'Fecha posterior'
        ]

    def __verified_accounts(self):
        is_valid = True
        missing_columns = []
        columns = list(self.df.columns)
        for column in columns:
            if column not in self.mandatory_columns:
                is_valid = False
                missing_columns.append(column)

        return is_valid, missing_columns


    def __clean_data(self):
        self.df["Importe del cargo"] = self.df["Importe del cargo"].replace(np.nan, 0)
        self.df["Importe del abono"] = self.df["Importe del abono"].replace(np.nan, 0)
        self.df["Fecha posterior"] = self.df["Fecha posterior"].apply(
            lambda row: str(row) if row is not None else ""
        )
        self.df = self.df.rename(
            columns={"País": "Pais", "Número de cuenta": "Numero de cuenta"}
        )

    def __remove_trash_key(self, item: dict):
        if "index" in item:
            item.pop("index")
        elif "level_0" in item:
            item.pop("level_0")
        return item

    def __change_key_name(self, item: dict):
        item["divisa"] = item.pop("Divisa")
        item["estatus"] = item.pop("Estatus de la cuenta")
        item["fecha"] = item.pop("Fecha posterior")
        item["abono"] = str(item.pop("Importe del abono"))
        item["cargo"] = str(item.pop("Importe del cargo"))
        item["descripcion"] = item.pop("Narrativa adicional")
        item["nombre"] = item.pop("Nombre de la cuenta")
        item["banco"] = item.pop("Nombre del banco")
        item["cuenta"] = str(item.pop("Numero de cuenta"))
        item["pais"] = item.pop("Pais")
        item["referencia_banco"] = str(item.pop("Referencia del Banco"))
        item["referencia_cliente"] = item.pop("Referencia del cliente")
        item["saldo"] = str(item.pop("Saldo"))
        item["tipo_trn"] = item.pop("Tipo TRN")
        item["tipo_cuenta"] = item.pop("Tipo de cuenta")
        return item

    def __get_account_statments(self, item: dict):
        account = {}
        account["cliente"] = str(item["Referencia del cliente"])
        account["empresa"] = ""
        account["banco"] = item["Nombre del banco"]
        account["cuenta"] = str(item["Numero de cuenta"])
        account["descripcion"] = item["Narrativa adicional"]
        account["referencia"] = str(item["Referencia del Banco"])
        account["fecha"] = item["Fecha posterior"]
        account["deposito"] = str(item["Importe del abono"])
        account["retiro"] = str(item["Importe del cargo"])
        account["saldo"] = str(item["Saldo"])
        return account

    def get_account_statment_dict(self):
        data = self.df
        data.reset_index(inplace=True)
        statment = data.to_dict("records")
        statment = list(map(self.__remove_trash_key, statment))
        statment = list(map(self.__change_key_name, statment))
        return statment

    def get_statment_dict(self, bank, client, company):
        data = self.df
        data.reset_index(inplace=True)
        statments = data.to_dict("records")
        statments = list(map(self.__get_account_statments, statments))
        return statments

    def save_statments(self, bank, client, company):
        is_valid, missing_columns = self.__verified_accounts()
        if not is_valid:
            raise Exception(MISSING_MESSAGE.format(str(missing_columns)))
        self.__clean_data()
        try:
            self.collection.insert_many(self.get_account_statment_dict())
            self.statments_collection.insert_many(
                self.get_statment_dict(bank, client, company)
            )
            return True
        except Exception as e:
            logger.error(e)
            return False
