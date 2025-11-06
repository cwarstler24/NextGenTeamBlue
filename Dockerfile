# Use official Python image
FROM python:3.13.8

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config.ini ./config.ini

# Expose port (change if your app uses a different port)
EXPOSE 8000

# Set environment variables (optional, for production best to use secrets)
# ENV VAR_NAME=value

# Start the app with Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
