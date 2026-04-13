FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# HF Spaces runs as user 1000 by default
RUN useradd -m -u 1000 user

WORKDIR /app

# System deps: libgl1/libglib2 for image processing, curl+unzip for Reflex bun install
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps (no torch needed — much lighter image)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Pre-build Reflex frontend during Docker build (as root, so bun/npm work)
# This avoids the 30-min runtime timeout on HF Spaces
RUN reflex init

# Fix ownership after all installs and builds
RUN chown -R user:user /app /home/user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# HF Spaces uses port 7860 by default
EXPOSE 7860

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "7860", "--single-port"]