FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create non-root user (required by HF Spaces)
RUN useradd -m -u 1000 user

WORKDIR /app

# Install system dependencies for OpenCV/Pix2TeX
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (torch CPU-only to save ~1.5 GB)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && \
    grep -v "^torch" /app/requirements.txt > /app/requirements_docker.txt && \
    pip install -r /app/requirements_docker.txt

# Copy application code
COPY . /app

# Initialize Reflex frontend (run as root so bun/npm install works)
RUN reflex init

# Fix ownership after all installs
RUN chown -R user:user /app /home/user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

EXPOSE 7860

CMD ["reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0", "--backend-port", "7860", "--single-port"]
