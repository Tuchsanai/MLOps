from omegaconf import OmegaConf

base_config = OmegaConf.load("config_base.yaml")
override_config = OmegaConf.load("config_override.yaml")

# Merge the two configs
merged_config = OmegaConf.merge(base_config, override_config)

print("Database Host:", merged_config.database.host)
print("Database Port:", merged_config.database.port)
print("Database User:", merged_config.database.user)
print("Database Password:", merged_config.database.password)