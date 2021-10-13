from os import environ

import pymongo
import pandas as pd
import numpy as np

from logger import logger


class AfirmeModel:
    def __init__(self, document):
        self.df = pd.read_excel(document)
        self.__db = pymongo.MongoClient(environ.get("MONGO_URI")).robin_hood
        self.afirme_collection = self.__db[environ.get("AFIRME_COLLECTION")]
        self.accounts_collection = self.__db[environ.get("ACCOUNT_STATMENT_COLLECTION")]
        self.valid_columns = [
            "Concepto",
            "Fecha (DD/MM/AA)",
            "Referencia",
            "Cargo",
            "Abono",
            "Saldo",
            "Cuenta",
            "Código",
            "No. Secuencia",
        ]
        self.__verified_document()
        self.__change_columns_name()
        self.__transform_data()

    def __verified_document(self):
        for column in list(self.df.columns):
            if column not in self.valid_columns:
                raise Exception("El archivo no es valido")

    def __change_columns_name(self):
        self.df = self.df.rename(
            columns={
                "Concepto": "concepto",
                "Fecha (DD/MM/AA)": "fecha",
                "Referencia": "referencia",
                "Cargo": "cargo",
                "Abono": "abono",
                "Saldo": "saldo",
                "Cuenta": "cuenta",
                "Código": "codigo",
                "No. Secuencia": "secuencia",
            }
        )
        self.df.pop("secuencia")

    def __transform_data(self):
        self.df["rastreo"] = self.df.concepto.str.extract(r"(?<=RASTREO )([^\s]+)")
        self.df.rastreo = self.df.rastreo.replace(np.nan, "")

        self.df["clabe"] = self.df.concepto.str.extract(r"(?<=CLABE )([^\s]+)")
        self.df.clabe = self.df.clabe.replace(np.nan, "")

        self.df["rfc"] = self.df.concepto.str.extract(r"(?<=RFC )([^\s]+)")
        self.df.rfc = self.df.rfc.replace(np.nan, "").replace("ND", "")

        self.df["descripcion"] = self.df.concepto.str.extract(
            r"(?<=HORA:\d{2}:\d{2}:\d{2} )(.+?(?=\sCLABE))"
        )
        self.df.descripcion = self.df.descripcion.replace(np.nan, "")

        self.df["hora"] = self.df.concepto.str.extract(r"(?<=HORA:)(\d{2}:\d{2}:\d{2})")
        self.df.hora = self.df.hora.replace(np.nan, "00:00:00")

        self.df.concepto = self.df.concepto.str.extract(r"(?<=CONCEPTO)(.+)")
        self.df.concepto = self.df.concepto.replace(np.nan, "")

        self.df.fecha = self.df.fecha.apply(lambda x: str(x))

    def __get_afirme_statments_dict(self):
        statments = self.df.to_dict("records")
        return statments

    def __make_account_statments_dict(self, item: dict) -> dict:
        statment = {
            "cliente": "",
            "empresa": "",
            "banco": "afirme",
            "cuenta": item["cuenta"],
            "descripcion": item["descripcion"],
            "referencia": item["referencia"],
            "fecha": item["fecha"],
            "deposito": item["abono"],
            "retiro": item["cargo"],
            "saldo": item["saldo"],
        }
        return statment

    def __get_account_statment(self):
        statments = self.df.to_dict("records")
        statments = list(map(self.__make_account_statments_dict, statments))
        return statments

    def save_statments(self):
        try:
            self.afirme_collection.insert_many(self.__get_afirme_statments_dict())
            self.accounts_collection.insert_many(self.__get_account_statment())
            return True
        except Exception as e:
            logger.error(e)
            return False
