from os import environ
from typing import Optional, List

from bson import ObjectId
import motor.motor_asyncio

from app.models.account_statment import AccountStatment


db_route = f"{environ.get('MONGO_URI')}robin_hood"
client = motor.motor_asyncio.AsyncIOMotorClient(db_route)
db = client.college


async def get_account_statments(filters: dict) -> Optional[List[AccountStatment]]:
    statments = (
        await db[environ.get("ACCOUNT_STATMENT_COLLECTION")].find(filters).to_list(100)
    )
    return statments
