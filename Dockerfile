# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /bot

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . .

# Expose bot
CMD ["python", "main.py"]
