# Dockerfile
# Stage 1: Build dependencies
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq5 \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN useradd --create-home appuser

# Copy application code
COPY --chown=appuser:appuser . /app/

# Create directories
RUN mkdir -p /app/staticfiles /app/logs && \
  chown -R appuser:appuser /app/staticfiles /app/logs

# Switch to non-root user
#USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=3 \
  CMD curl http://localhost:8000/authenticated/ || exit 1

# Run gunicorn with dynamic workers based on CPU cores
# Formula: (2 × CPU cores) + 1
CMD ["sh", "-c", "gunicorn mysite.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers $((2 * $(nproc) + 1)) \
  --threads 2 \
  --worker-class gthread \
  --access-logfile - \
  --error-logfile -"]