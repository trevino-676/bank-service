from fastapi import APIRouter, UploadFile, File, status
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/v1/upload", tags=["upload files"])


@router.post("/{bank}")
def upload_file(bank: str, file: UploadFile = File(...)):
    return {"filename": file.filename, "bank": bank, "type": len(file.file)}

