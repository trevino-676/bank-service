from os import environ

import pandas as pd
import numpy as np
import pymongo


class HSBCModel:
    def __init__(self, document):
        self.df = pd.read_excel(document)
        self.__client = pymongo.MongoClient(environ.get("MONGO_URI"))
        self.__db = self.__client.robin_hood
        self.collection = self.__db[environ.get("HSBC_COLLECTION")]
        self.statments_collection = self.__db["ACCOUNT_STATMENT_COLLECTION"]

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
        item["cuenta"] = item.pop("N√∫mero de cuenta")
        item["pais"] = item.pop("Pa√≠s")
        item["referencia_banco"] = str(item.pop("Referencia del Banco"))
        item["referencia_cliente"] = item.pop("Referencia del cliente")
        item["saldo"] = str(item.pop("Saldo"))
        item["tipo_trn"] = item.pop("Tipo TRN")
        item["tipo_cuenta"] = item.pop("Tipo de cuenta")
        return item

    def get_account_statment_dict(self):
        self.df.reset_index(inplace=True)
        statment = self.df.to_dict("record")
        statment = list(map(self.__remove_trash_key, statment))
        statment = list(map(self.__change_key_name, statment))
        return statment

    def get_statment_dict(self, bank, client, company):
        statments = []
        for item in self.df:
            statment = {
                "cliente": client,
                "empresa": company,
                "banco": bank,
                "cuenta": item["Numero de cuenta"],
                "descripcion": item["Narrativa adicional"],
                "referencia": item["Referencia del Banco"],
                "fecha": item["Fecha posterior"],
                "deposito": str(item["Importe del abono"]),
                "retiro": str(item["Importe del cargo"]),
                "saldo": str(item["Saldo"]),
            }
            statments.append(statment)
        return statments

    def save_statments(self, bank, client, company):
        self.__clean_data()
        try:
            self.collection.insert_many(self.get_account_statment_dict())
            self.statments_collection.insert_many(
                self.get_statment_dict(bank, client, company)
            )
            return True
        except Exception as e:
            # TODO: create logger
            print(e)
            return False
