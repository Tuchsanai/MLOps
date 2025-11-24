## 🛠️ Applying the Lab with Docker-Compose

To run the MLflow server using **Docker-Compose** instead of the long `docker run` command in Step 1, you will create a configuration file named `docker-compose.yaml` (or `docker-compose.yml`) in your main lab folder.

This approach offers a cleaner, more repeatable way to define and manage multi-container applications.

### Step 0 (Modified) - Prepare Working Directory

The preparation steps remain the same, but you will also create the `docker-compose.yaml` file.

1.  **Create and enter the lab folder:**

    ```bash
    mkdir -p mlflow-lab
    cd mlflow-lab
    ```

2.  **Create persistent folders:**

    ```bash
    # Check for mlruns_db
    if [ ! -d "mlruns_db" ]; then
        mkdir mlruns_db
        echo "✅ Created 'mlruns_db' folder."
    else
        echo "ℹ️ 'mlruns_db' folder already exists."
    fi

    # Check for mlartifacts
    if [ ! -d "mlartifacts" ]; then
        mkdir mlartifacts
        echo "✅ Created 'mlartifacts' folder."
    else
        echo "ℹ️ 'mlartifacts' folder already exists."
    fi
    ```

3.  **Create the `docker-compose.yaml` file.**

    Create a file named `docker-compose.yaml` in the `mlflow-lab` directory with the following content:

    ```yaml
    version: '3.8'

    services:
      mlflow-server:
        # Use the official MLflow image
        image: ghcr.io/mlflow/mlflow
        # Name the container
        container_name: mlflow-server
        # Expose port 5000 for the UI/API
        ports:
          - "5000:5000"
        # Define persistent storage volumes
        volumes:
          # Map local 'mlruns_db' to container's DB directory
          - ./mlruns_db:/mlflow/db
          # Map local 'mlartifacts' to container's artifacts directory
          - ./mlartifacts:/mlflow/artifacts
        # The command to start the MLflow server
        command: >
          mlflow server
          --host 0.0.0.0
          --port 5000
          --backend-store-uri sqlite:////mlflow/db/mlflow.db
          --default-artifact-root /mlflow/artifacts
        # Ensure the server restarts if it fails
        restart: unless-stopped
    ```

4.  **Verify the folder structure**

    ```bash
    ls -F
    ```

    > **✅ Expected Output:**
    > You should now see the two folders and the `docker-compose.yaml` file:

    > ```text
    > docker-compose.yaml
    > mlartifacts/
    > mlruns_db/
    > ```

-----

### Step 1 (Modified) – Start MLflow Server with Docker-Compose

Instead of the lengthy `docker run` command, you'll use a single `docker-compose` command.

Run the following command **inside the `mlflow-lab` folder**:

```bash
docker-compose up -d
```

| Docker-Compose Command Part | Function |
| :--- | :--- |
| `docker-compose up` | Builds (if necessary) and starts the services defined in `docker-compose.yaml`. |
| `-d` | Runs the containers in **detached mode** (in the background). |

Check that the container is running:

```bash
docker ps
```

You should see `mlflow-server` in the list, confirming it was started by Docker-Compose.

-----

### Step 2 – Open MLflow UI

1.  Open a browser and go to:

    **[http://localhost:5000](https://www.google.com/search?q=http://localhost:5000)**

2.  You should see the **MLflow UI** (Experiments page).

-----

### 🛑 Stopping the Server

When the lab is complete, you can stop and remove the server using Docker-Compose:

Run the following command **inside the `mlflow-lab` folder**:

```bash
docker-compose down
```

| Docker-Compose Command Part | Function |
| :--- | :--- |
| `docker-compose down` | Stops the running containers and removes the containers and default network. |

This will stop the `mlflow-server` container, but it **will keep** your persistent data in the `mlruns_db` and `mlartifacts` folders, allowing you to restart the server later without losing data.

