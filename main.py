from typing import Union

from fastapi import FastAPI, File, UploadFile
from detect_cccd import DetectCCCD
import os
import asyncio

app = FastAPI()

# Đường dẫn lưu trữ tệp
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/extract-document/")
async def extract_document(front: UploadFile = File(...), back: UploadFile = File(...)):
    file_location_front = os.path.join(UPLOAD_FOLDER, front.filename)
    file_location_back = os.path.join(UPLOAD_FOLDER, back.filename)
    
    # Lưu file
    with open(file_location_front, "wb") as buffer:
        buffer.write(await front.read())

    with open(file_location_back, "wb") as buffer:
        buffer.write(await back.read())
    
    model = DetectCCCD(file_location_front, file_location_back)
    results = await asyncio.gather(model.detect_cccd_front(), model.detect_cccd_back())
    detect_front = results[0]

    return {"message":  "successfully", "object": detect_front}
