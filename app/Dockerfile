# Use official Python slim image as base
FROM python:3.13.3-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt first (for layer caching)
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Default command to run your Python script
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
