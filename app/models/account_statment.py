from pydantic import BaseModel, Field
from bson import ObjectId

from app.models import PyObjectId


class AccountStatment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    cliente: str = Field(...)
    empresa: str = Field(...)
    banco: str = Field(...)
    cuenta: str = Field(...)
    descripcion: str = Field(...)
    referencia: str = Field(...)
    fecha: str = Field(...)
    deposito: str = Field(...)
    retiro: str = Field(...)
    saldo: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "cliente": "Joe Doe",
                "empresa": "drumbot",
                "banco": "bbva",
                "cuenta": "012014013",
                "descripcion": "Compra de equipo de computo",
                "referencia": "AXSO015MX",
                "fecha": "2021-10-08",
                "deposito": "0.0",
                "retiro": "10000.00",
                "saldo": "150237.54",
            }
        }
