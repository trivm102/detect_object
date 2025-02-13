# Dùng image nhẹ hơn để giảm kích thước
FROM python:3.9-slim  

# Đặt thư mục làm việc
WORKDIR /app  

# Copy file vào container
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  

COPY . .  

# Chạy FastAPI bằng Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
