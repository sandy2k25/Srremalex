FROM python:3.11-slim

# Create non-root user (HF requirement)
RUN useradd -m -u 1000 user

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p static

# Set proper permissions
RUN chown -R user:user /app

# Switch to non-root user
USER user

# Expose port 7860 (required by HF Spaces)
EXPOSE 7860

# Use Gunicorn for production deployment
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "2", "--timeout", "120", "docker_app:app"]