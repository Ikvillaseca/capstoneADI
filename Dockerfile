# Use official Python 3.13 image (replace with correct tag if needed)
FROM python:3.13.7-slim

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY dev-requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r dev-requirements.txt

# Copy project files
COPY . .

# Expose port (default Django port)
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]