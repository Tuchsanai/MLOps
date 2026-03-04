# ──────────────────────────────────────────
# Backend Dockerfile — Flask + Gemini API
# ──────────────────────────────────────────
FROM python:3.11-slim

# ตั้ง working directory ภายใน container
WORKDIR /app

# คัดลอกไฟล์ requirements แล้วติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอก source code ทั้งหมด
COPY . .

# เปิด port 8000
EXPOSE 8000

# รัน Flask application
CMD ["python", "app.py"]
