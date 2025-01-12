
from omegaconf import OmegaConf

# Load the YAML configuration file correctly
config = OmegaConf.load("config.yaml")

# Access values from the configuration
print("Server Host:", config.server.host)
print("Server Port:", config.server.port)
print("Client URL:", config.client.url)
print("Client Server Port:", config.client.server_port)

# # Modifying a value in the config
# config.server.port = 8080

# # Re-check the updated values with interpolation
# print("Updated Server Port:", config.server.port)
# print("Updated Client URL:", config.client.url)
