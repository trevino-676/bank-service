from typing import Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from bson.json_util import dumps

from app.services.account_statments_service import AccountStatmentsService


router = APIRouter(prefix="/v1/account/statments", tags=["Account statments"])


@router.get("/movements")
def get_account_statments_by_movements(
    bank: Optional[str] = None,
    company: Optional[str] = None,
    account: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
):
    filters = {}
    if bank:
        filters["banco"] = bank
    elif company:
        filters["empresa"] = company
    elif account:
        filters["cuenta"] = account
    elif from_date and to_date:
        filters["fecha"] = {"$gte": from_date, "$lte": to_date}

    response_headers = {"Content-Type": "applicaction/json"}
    service = AccountStatmentsService()
    statments = service.get_movements(filters)

    if not statments:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dumps({"message": "No se encontraron movimientos bancarios"}),
            headers=response_headers,
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dumps(statments),
        headers=response_headers,
    )


@router.get("/by_day")
def get_account_statments_by_day(
    bank: Optional[str] = None,
    company: Optional[str] = None,
    account: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
):
    filters = {}
    if bank:
        filters["banco"] = bank
    elif company:
        filters["empresa"] = company
    elif account:
        filters["cuenta"] = account
    elif from_date and to_date:
        filters["fecha"] = {"$gte": from_date, "$lte": to_date}

    response_headers = {"Content-Type": "application/json"}
    service = AccountStatmentsService()
    movements = service.get_daily_group_movements(filters)

    if not movements:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dumps({"message": "No se encontraron movimientos bancarios"}),
            headers=response_headers,
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dumps(movements),
        headers=response_headers,
    )
