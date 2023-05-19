from fastapi import APIRouter, UploadFile, File
from repository.UploadRepo import insert_excel_data

router = APIRouter()

@router.post("/upload")
async def upload_product(file: UploadFile = File(...)):
    content = await file.read()
    return_response = insert_excel_data(content)
    return return_response
