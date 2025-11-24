# Base image: Ubuntu 25.04 (Plucky Puffin)
FROM ubuntu:25.04

# ----------------------------------------------------
# Configuration & Environment Variables
# ----------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    # FIX 1: Move venv to /home/student/ so the user has permission to write to it
    VIRTUAL_ENV=/home/mlops_venv

# FIX 2: Define PATH in a separate ENV instruction to ensure $VIRTUAL_ENV is loaded
ENV PATH="$VIRTUAL_ENV/bin:/home/student/.local/bin:$PATH"

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
# 4. Install uv, Create VENV, and Configure Shell
# ----------------------------------------------------
# FIX 3: We added --seed to install pip/setuptools
# This will now succeed because $VIRTUAL_ENV is inside /home/student/
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /home/student/.local/bin/uv venv "$VIRTUAL_ENV" --seed && \
    echo "source ${VIRTUAL_ENV}/bin/activate" >> /home/student/.bashrc

# ----------------------------------------------------
# 5. Install Python Packages into the VENV
# ----------------------------------------------------
RUN uv pip install --python "$VIRTUAL_ENV/bin/python" \
    jupyterlab \
    ipykernel \
    pandas \
    scikit-learn \
    opencv-python-headless

# ----------------------------------------------------
# 6. Register Jupyter Kernel
# ----------------------------------------------------
RUN python -m ipykernel install --user \
    --name=mlops-env \
    --display-name="Python (MLOps Venv)"

# ----------------------------------------------------
# 7. JupyterLab startup
# ----------------------------------------------------
EXPOSE 8888

# ----------------------------------------------------
# 7. JupyterLab startup
# ----------------------------------------------------
EXPOSE 8888

# Added --notebook-dir=/home/student
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--IdentityProvider.token='mlops'", "--notebook-dir=/home/student"]