from io import BytesIO

from fastapi import APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse

from app.services.hsbc_service import HSBCService


router = APIRouter(prefix="/v1/upload", tags=["upload files"])


@router.post("/{bank}")
def upload_file(bank: str, file: UploadFile = File(...)):
    process_file(bank, BytesIO(file.file.read()))
    return JSONResponse(bank, status.HTTP_200_OK)


def process_file(bank: str, file):
    if bank.lower() == "hsbc":
        service = HSBCService(file)

    service.save_statments(bank)
