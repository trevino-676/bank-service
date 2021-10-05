from os import environ

import pandas as pd
import numpy as np
import pendulum

from app.models import db
from logger import logger


MISSING_MESSAGE= "El archivo es incorrecto. Faltan las siguientes columnas: {}"


class BanorteModel:
    def __init__(self, document):
        self.df = pd.read_csv(document)
        self.banorte_collection = db[environ.get("BANORTE_COLLECTION")]
        self.account_statment = db[environ.get("ACCOUNT_STATMENTS_COLLECTION")]
        self.__verification_list = [
            'CUENTA',
            'FECHA DE OPERACIÓN',
            'FECHA',
            'REFERENCIA',
            'DESCRIPCIÓN',
            'COD. TRANSAC',
            'SUCURSAL',
            'DEPÓSITOS',
            'RETIROS',
            'SALDO',
            'MOVIMIENTO',
            'DESCRIPCIÓN DETALLADA',
            'CHEQUE'
        ]

    def verify_statments(self):
        verified = True
        missing_columns = []
        columns = list(self.df.colums)
        for column in columns:
            if column not in self.__verification_list:
                verified = False
                missing_columns.append(column)

        return verified, missing_columns

    def __convert_currency_to_str(self, currency: str) -> str:
        cleaned_currency = currency[1:]
        cleaned_currency = cleaned_currency.replace(",", "").replace(".", "")
        return cleaned_currency

    def __convert_date_to_common_date(self, date: str) -> str:
        return pendulum.from_format(date, "DD/MM/YYYY").format("YYYY-MM-DD")

    def __rename_columns(self):
        self.df = self.df.rename(columns={
            "CUENTA": "cuenta",
            "FECHA DE OPERACIÓN": "fecha_operacion",
            "FECHA": "fecha",
            "REFERENCIA": "referencia",
            "DESCRIPCIÓN": "descripcion",
            "COD. TRANSAC": "codigo_transaccion",
            "SUCURSAL": "sucursal",
            "DEPÓSITOS": "deposito",
            "RETIROS": "retiro",
            "SALDO": "saldo",
            "MOVIMIENTO": "movimiento",
            "DESCRIPCIÓN DETALLADA": "descripcion",
            "CHEQUE": "cheque"
        })

    def __clean_data(self):
        self.__rename_columns()
        self.df.cheque = self.df.cheque.replace("-". "")
        self.df.deposito = (self.df.deposito.replace("-", "00")
                            .apply(self.__convert_currency_to_str))
        self.df.descripcion = self.df.descripcion.replace("-", "")
        self.df.retiro = (self.df.retiro.replace("-", "00")
                          .apply(self.__convert_currency_to_str))
        self.df.saldo = (self.df.saldo.replace("-", "00")
                         .apply(self.__convert_currency_to_str))
        self.df.fecha = self.df.fecha.apply(self.__convert_date_to_common_date)
        self.df.fecha_operacion = (self.df.fecha_operacion
                                   .apply(self.__convert_date_to_common_date))
        self.df.drop("index")

    def __get_banorte_statments(self):
        statments = self.df.to_dict("records")
        return statments

    def __make_account_statments_dict(self, item: dict):
        statments = {}
        statments["cliente"] = ""
        statments["empresa"] = ""
        statments["banco"] = "Banorte"
        statments["cuenta"] = item["cuenta"]
        statments["descripcion"] = item["descripcion"]
        statments["referencia"] = item["referencia"]
        statments["fecha"] = item["fecha"]
        statments["deposito"] = item["deposito"]
        statments["retiro"] = item["retiro"]
        statments["saldo"] = item["saldo"]
        return statments

    def __get_acount_statments(self):
        statments = self.df.to_dict("records")
        statments = list(map(self.__make_account_statments_dict, statments))
        return statments

    def save_statments(self):
        is_valid, missing_fields = self.verify_statments()
        if not is_valid:
            raise Exception(MISSING_MESSAGE.format(str(missing_fields)))
        try:
            self.__clean_data()
            self.banorte_collection.insert_many(self.__get_banorte_statments())
            self.account_statment.insert_many(self.__get_acount_statments())
            return True
        except Exception as e:
            logger.error(e)
            return False



























