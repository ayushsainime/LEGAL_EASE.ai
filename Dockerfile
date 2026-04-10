FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN useradd -m -u 1000 user

WORKDIR /app

# System deps: libgl1/libglib2 for OpenCV, curl+unzip for Reflex bun install
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps — use CPU-only torch to save ~1.5 GB download time
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    grep -v "^torch" /app/requirements.txt > /app/requirements_docker.txt && \
    pip install -r /app/requirements_docker.txt

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

EXPOSE 7860

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "7860", "--single-port"]