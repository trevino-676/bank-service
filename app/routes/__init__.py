from io import BytesIO

from fastapi import APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse

from app.services.hsbc_service import HSBCService
from app.services.banorte_service import BanorteService
from app.services.bbva_service import BBVAService


router = APIRouter(prefix="/v1/upload", tags=["upload files"])


@router.post("/{bank}")
def upload_file(bank: str, file: UploadFile = File(...)):
    process_file(bank, BytesIO(file.file.read()))
    return JSONResponse(bank, status.HTTP_200_OK)


def process_file(bank: str, file):
    service = None
    bank = bank.lower()
    if bank == "hsbc":
        service = HSBCService(file)
        service.save_statments(bank)
        return
    elif bank == "bbva":
        service = BBVAService(file)
    elif bank == "banorte":
        service = BanorteService(file)

    service.save_statments()

