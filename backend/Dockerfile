FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create volume directories
RUN mkdir -p /data
RUN mkdir -p /app/uploads

# Copy the rest of the application
COPY . .

# Set environment variables
ENV DATABASE_URL="sqlite:////data/h2s_sentinel.db"
ENV UPLOAD_DIR="/app/uploads"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
