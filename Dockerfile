# Use a slim Python image with 3.10 (compatible with tflite-runtime)
FROM python:3.10-slim

# Install system packages required by OpenCV headless
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Expose port for Render/Fly (they set $PORT env var)
ENV PORT=8080
EXPOSE 8080

# Gunicorn is lightweight and production-grade
CMD gunicorn --bind 0.0.0.0:${PORT} app:app
