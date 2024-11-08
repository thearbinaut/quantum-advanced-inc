FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Run as non-root user
RUN adduser --disabled-password --gecos '' myuser
USER myuser

# Run gunicorn
CMD gunicorn --chdir src/control_room --bind 0.0.0.0:$PORT wsgi:app
