FROM python:3.11-slim

# Create a non‑root user
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

# Create a volume for persistent database storage
VOLUME ["/data"]

ENV USER_DB=/data/users.db
ENV PORT=5001

USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:5001", "app:create_app()", "--workers", "2"]