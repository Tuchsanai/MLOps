# Base image: Ubuntu 25.04 (Plucky Puffin)
FROM ubuntu:25.04

# Set environment variables to non-interactive to avoid prompts during build
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/home/student/.cargo/bin:/home/student/mlops_venv/bin:$PATH" \
    VIRTUAL_ENV=/home/student/mlops_venv

# ----------------------------------------------------
# 1. System Dependencies & Package Installation
# ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    python3 \
    python3-dev \
    python3-venv \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# 2. Install Docker Client (docker-ce-cli)
# ----------------------------------------------------
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu noble stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# 3. User Setup
# ----------------------------------------------------
RUN useradd -m -s /bin/bash student
USER student
WORKDIR /home/student

# ----------------------------------------------------
# 4. Install uv & Create Python Virtual Environment
# ----------------------------------------------------
# uv installer puts the binary into ~/.cargo/bin (already on PATH)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv venv "$VIRTUAL_ENV"

# ----------------------------------------------------
# 5. Install Python Packages into the VENV (explicit python)
# ----------------------------------------------------
RUN uv pip install --python "$VIRTUAL_ENV/bin/python" \
    jupyterlab \
    ipykernel \
    pandas \
    scikit-learn \
    opencv-python-headless

# ----------------------------------------------------
# 6. Register Jupyter Kernel from the VENV
# ----------------------------------------------------
RUN "$VIRTUAL_ENV/bin/python" -m ipykernel install --user \
    --name=mlops-env \
    --display-name="Python (MLOps Venv)"

# ----------------------------------------------------
# 7. JupyterLab startup
# ----------------------------------------------------
EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
