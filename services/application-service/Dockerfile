FROM python:3.11-slim

RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

VOLUME ["/data"]

ENV APPLICATION_DB=/data/applications.db
ENV PORT=5003

USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:5003", "app:create_app()", "--workers", "2"]