# Small official Python image
FROM python:3.12-slim

# Don't write .pyc files, don't buffer logs (so `docker logs` is live)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first -> Docker caches this layer until they change
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Security: don't run as root
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

# Container is marked unhealthy if /health stops answering
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://localhost:5000/health', timeout=2)" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
