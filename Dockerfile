# Dockerfile
# Stage 1: Build stage
FROM python:3.13-slim AS builder

# Make app directory
RUN mkdir /app

# Set working directory in container
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-slim AS runtime

# Create non-root user
RUN useradd -m -r appuser && \
  mkdir /app && \
  chown -R appuser /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq5 \
  curl \
  gosu \
  && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies from the build stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser . .

# Create directories
RUN mkdir -p /app/staticfiles && \
  chown -R appuser /app/staticfiles

# Make the startup script executable.
RUN chmod +x /app/entrypoint.sh

# Optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Run gunicorn with dynamic workers based on CPU cores
# Number of workers formula: (2 × CPU cores) + 1
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mysite.wsgi:application"]