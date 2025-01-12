


# LAB: OmegaConf on Ubuntu 

This lab focuses on working with `OmegaConf` for configuration management using YAML files in a Python environment. It assumes you are working on an Ubuntu system without Python pre-installed.



## Objective:
- Learn how to set up Python in an Ubuntu system without Python installed.
- Use `OmegaConf` to load, modify, and merge YAML configurations.
- Work with environment variable resolutions using `OmegaConf`.



## Prerequisites:
- Ubuntu system with no Python pre-installed.
- Internet access.
- Basic familiarity with the command line.



## Lab Setup:

1. **Install Python and Pip:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```

2. **Clone the Git Repository:**
   ```bash
   git clone https://github.com/Tuchsanai/MLOps.git
   cd MLOps/02_Auto_DataVersion_AND_MLCyCle/week07/LAB01
   
   ```

3. **Create a Python Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```
   If no `requirements.txt` exists, create it with the following content:
   ```
   omegaconf
   ```

---

## File Overview:

- **`app.py`:** Main Python script using OmegaConf for YAML parsing and modification.
- **`config.yaml`:** Configuration file defining server and client settings.

### `config.yaml`
```yaml
server:
  host: localhost
  port: 80
client:
  url: http://${server.host}:${server.port}/
  server_port: ${server.port}
```

### `app.py`
```python
from omegaconf import OmegaConf

# Load the YAML configuration file
config = OmegaConf.load("config.yaml")

# Accessing values
print("Server Host:", config.server.host)
print("Server Port:", config.server.port)
print("Client URL:", config.client.url)
print("Client Server Port:", config.client.server_port)
```

---

## Lab Activities:

**Load Configuration:**
   - Run the `app.py` script and observe how the `config.yaml` values are loaded and displayed.


---

## Running the Lab:

```bash
python app.py
```

---

## Expected Output:
```plaintext
Server Host: localhost
Server Port: 80
Client URL: http://localhost:80/
Client Server Port: 80
```

---

## Cleanup:

```bash
deactivate
rm -rf venv
```

---

## Grading Criteria:
- Correct installation and setup.
- Proper loading and modification of YAML configurations.
- Demonstration of interpolation and environment variable usage.
```
