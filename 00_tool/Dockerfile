# Base image: Ubuntu 25.04
FROM ubuntu:25.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    nano \
    python3 \
    python3-dev \
    python3-venv \
    python-is-python3 \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    gnupg \
    tree \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate venv by adding to PATH (this affects all subsequent RUN commands)
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages (now uses venv's pip automatically)
RUN pip install --upgrade pip && \
    pip install \
    jupyterlab \
    ipykernel \
    pandas \
    scikit-learn \
    opencv-python-headless \
    "mlflow[extras]"

# PyTorch CPU-only
RUN pip install \p
    torch torchvision \
    --index-url https://download.pytorch.org/whl/cpu

# Register the venv kernel with Jupyter
RUN python -m ipykernel install --name=mlops --display-name="Python (mlops)"

# Set working directory
WORKDIR /home/student/workspace

# Ensure the directory exists
RUN mkdir -p /home/student/workspace

# CMD will also use venv because of ENV PATH
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/home/student/workspace", "--IdentityProvider.token=mlops"]