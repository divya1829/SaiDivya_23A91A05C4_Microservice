# ============================
# Stage 1: Builder
# ============================
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


# ============================
# Stage 2: Runtime
# ============================
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y cron tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Copy dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY app /app/app
COPY scripts /app/scripts
COPY cron /app/cron
COPY student_private.pem /app/student_private.pem
COPY entrypoint.sh /entrypoint.sh

# Setup cron
RUN chmod 0644 /app/cron/2fa-cron && \
    crontab /app/cron/2fa-cron

# Create volume mount points
RUN mkdir -p /data /cron

# Expose API port
EXPOSE 8080

# Start cron + API
ENTRYPOINT ["/entrypoint.sh"]
