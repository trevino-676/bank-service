from typing import Optional

from fastapi import APIRouter

from app.services.account_statments_service import get_account_statments


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

    # response_headers = {"Content-Type": "applicaction/json"}

    statments = get_account_statments(filters)
    return statments
