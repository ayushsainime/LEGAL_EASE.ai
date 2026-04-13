FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# HF Spaces runs as user 1000
RUN useradd -m -u 1000 user

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    unzip \
    curl \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install bun (Reflex needs it for frontend builds)
RUN curl -fsSL https://bun.sh/install | BUN_INSTALL="/usr/local" bash

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Remove old math service files that would cause import errors
RUN rm -f /app/backend/services/math_ocr_service.py \
           /app/backend/services/math_service.py \
           /app/backend/services/tutor_service.py \
           /app/backend/services/__pycache__/math_ocr_service*.pyc \
           /app/backend/services/__pycache__/math_service*.pyc \
           /app/backend/services/__pycache__/tutor_service*.pyc \
           /app/backend/__pycache__/*.pyc \
    || true

# Pre-build Reflex frontend during Docker build
ENV HOME=/root
RUN reflex init

# Fix ownership after all installs and builds
RUN chown -R user:user /app /home/user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:/usr/local/bin:$PATH \
    PORT=7860

EXPOSE 7860

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--single-port"]
