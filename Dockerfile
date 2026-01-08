# Multi-stage Dockerfile for Voice Cloning System
# Base: Python 3.11 with CUDA support

FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3-pip \
    python3.11-venv \
    portaudio19-dev \
    libsndfile1 \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create symlinks for python3.11
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# Create non-root user for security
RUN useradd -m -u 1000 voiceuser && \
    mkdir -p /app && \
    chown -R voiceuser:voiceuser /app

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install "transformers>=4.33.0,<4.37.0" && \
    pip install TTS && \
    pip install -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY *.py ./
COPY voices/README.md ./voices/README.md

# Create necessary directories
RUN mkdir -p voices/my_voice outputs models

# Set permissions and ownership
RUN chmod +x quick_clone.py cli.py web_ui.py scripts/*.py && \
    chown -R voiceuser:voiceuser /app

# Expose port for web UI
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Switch to non-root user
USER voiceuser

# Default command: show help
CMD ["python3", "cli.py", "--help"]

# Optional: Web UI as entrypoint
# CMD ["python3", "web_ui.py", "--host", "0.0.0.0"]
