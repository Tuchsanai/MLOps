# Base image: Ubuntu 25.04
FROM ubuntu:25.04

# ----------------------------------------------------
# 0. Environment Setup
# ----------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/home/student/mlops_venv \
    PATH="/home/student/mlops_venv/bin:/home/student/.local/bin:$PATH"

# ----------------------------------------------------
# 1. System Dependencies
# ----------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
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
# 3. User Setup
# ----------------------------------------------------
RUN useradd -m -s /bin/bash student

# [CRITICAL] Add student to docker group (Must be done as root before switching users)
RUN groupadd -f docker && usermod -aG docker student

# Switch to user
USER student

# Create the workspace directory
RUN mkdir -p /home/student/workspace

# Set the default working directory
WORKDIR /home/student/workspace

# ----------------------------------------------------
# 4. Install uv & Create VENV
# ----------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /home/student/.local/bin/uv venv "$VIRTUAL_ENV" --seed && \
    echo "source ${VIRTUAL_ENV}/bin/activate" >> /home/student/.bashrc

# ----------------------------------------------------
# 5. Install Python Packages
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
# 7. Startup
# ----------------------------------------------------
EXPOSE 8888

# Jupyter will launch in the WORKDIR (/home/student/workspace) automatically
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--IdentityProvider.token='mlops'"]