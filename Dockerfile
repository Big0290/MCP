FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ENVIRONMENT=production
ENV DB_PATH=/app/data/agent_tracker.db

# Conversation tracking defaults
ENV ENABLE_BACKGROUND_MONITORING=true
ENV MONITORING_INTERVAL_SECONDS=300
ENV ENABLE_AUTOMATIC_METADATA=true

# Logging defaults
ENV LOG_LEVEL=INFO
ENV LOG_FILE=/app/logs/agent_tracker.log

# Performance defaults
ENV MAX_EXECUTION_TIME_MS=30000
ENV BATCH_LOG_SIZE=100

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Create data and logs directories for persistent storage
RUN mkdir -p /app/data /app/logs

# Copy requirements files
COPY pyproject.toml requirements.txt ./

# Install dependencies - try pyproject.toml first, fallback to requirements.txt
RUN pip install --upgrade pip && \
    (pip install -e . || pip install -r requirements.txt) && \
    # Verify key dependencies are installed
    python -c "import mcp, sqlalchemy; print('✅ Dependencies installed successfully')"

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Make scripts executable and ensure proper ownership
RUN chmod +x docker-entrypoint.sh init_db.py docker-entrypoint.py && \
    chown app:app docker-entrypoint.sh init_db.py docker-entrypoint.py

# Switch to app user
USER app

# Expose port (if needed for health checks)
EXPOSE 8000

# Health check - use python directly since we're not using virtual environment
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c 'from models import get_session_factory; get_session_factory()()' || exit 1

# Set the entrypoint using Python directly
ENTRYPOINT ["python", "docker-entrypoint.py"]
