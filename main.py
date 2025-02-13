
from fastapi import FastAPI
import os

app = FastAPI()

# Đường dẫn lưu trữ tệp
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}
