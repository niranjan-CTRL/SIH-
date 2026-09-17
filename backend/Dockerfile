FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (needed for OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
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

# Pre-generate synthetic calibration and train AI model at container build time
RUN python -m app.ai.generate_synthetic_calibration && python -m app.ai.train_model

# Set environment variables
ENV DATABASE_URL="sqlite:////data/h2s_sentinel.db"
ENV UPLOAD_DIR="/app/uploads"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
