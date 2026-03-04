# ──────────────────────────────────────────
# Frontend Dockerfile — Python HTTP Server
# ──────────────────────────────────────────
FROM python:3.11-alpine

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ HTML
COPY index.html .

# เปิด port 80
EXPOSE 80

# รัน Python built-in HTTP server
CMD ["python", "-m", "http.server", "80"]
