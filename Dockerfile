# Build stage
FROM python:3.9-slim-buster as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim-buster

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

RUN adduser --disabled-password --gecos '' myuser
USER myuser

CMD gunicorn --chdir src/control_room --bind 0.0.0.0:$PORT wsgi:app
