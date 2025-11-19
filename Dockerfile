# Multi-stage build for optimal image size
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set metadata
LABEL maintainer="security@yourdomain.com" \
      description="Impossible Travel Detection Engine" \
      version="1.0.0"

# Create non-root user for security
RUN useradd -m -u 1000 detector && \
    mkdir -p /app /data /output && \
    chown -R detector:detector /app /data /output

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/detector/.local

# Copy application code
COPY --chown=detector:detector . .

# Switch to non-root user
USER detector

# Add local bin to PATH
ENV PATH=/home/detector/.local/bin:$PATH

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Volume for input/output data
VOLUME ["/data", "/output"]

# Default command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"
