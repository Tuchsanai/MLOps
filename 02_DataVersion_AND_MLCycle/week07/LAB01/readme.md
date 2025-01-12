Below is an updated `README.md` with three additional labs. Each lab follows a similar structure: objectives, prerequisites, lab setup, file overviews (if needed), lab activities, running the lab, and expected output.

---

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
- **Load Configuration**: Run the `app.py` script and observe how the `config.yaml` values are loaded and displayed.

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

# LAB 2: Merging Multiple YAML Configs with OmegaConf

In this lab, you will learn how to merge multiple YAML configuration files using `OmegaConf`. This is useful when you have a base configuration and want to override or extend it with environment-specific configs or user-provided settings.

## Objective:
- Understand how to merge multiple YAML config files into one `OmegaConf` object.
- Practice layering configs (e.g., base + environment + overrides).

## Prerequisites:
- Completion of **LAB: OmegaConf on Ubuntu** or equivalent knowledge.
- Python 3 and `omegaconf` installed in your virtual environment.

## Lab Setup:
1. **In the same directory**, create two YAML files: `config_base.yaml` and `config_override.yaml`.
2. **Create or update** a Python script named `merge_configs.py`.

### `config_base.yaml`
```yaml
database:
  host: localhost
  port: 5432
  user: default_user
  password: default_pass
```

### `config_override.yaml`
```yaml
database:
  user: override_user
  password: override_pass
```

### `merge_configs.py`
```python
from omegaconf import OmegaConf

base_config = OmegaConf.load("config_base.yaml")
override_config = OmegaConf.load("config_override.yaml")

# Merge the two configs
merged_config = OmegaConf.merge(base_config, override_config)

print("Database Host:", merged_config.database.host)
print("Database Port:", merged_config.database.port)
print("Database User:", merged_config.database.user)
print("Database Password:", merged_config.database.password)
```

## Lab Activities:
- **Inspect Base Config**: See what defaults are in `config_base.yaml`.
- **Inspect Override Config**: Note the fields that are being overridden.
- **Merge**: Run `merge_configs.py` and see how the final config differs from the base.

## Running the Lab:
```bash
python merge_configs.py
```

## Expected Output:
```plaintext
Database Host: localhost
Database Port: 5432
Database User: override_user
Database Password: override_pass
```

