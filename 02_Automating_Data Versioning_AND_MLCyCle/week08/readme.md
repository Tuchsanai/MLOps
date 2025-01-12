Okay, here's a Python lab focusing on `OmegaConf` and YAML, designed to be educational and hands-on.

**Lab Title: Mastering Configuration with OmegaConf and YAML**

**Objective:**

*   Understand how to define and load configurations using YAML.
*   Learn the core features of `OmegaConf` for accessing, manipulating, and merging configurations.
*   Practice using `OmegaConf` in a realistic scenario involving multiple configuration sources.

**Prerequisites:**

*   Python 3.7 or higher
*   `omegaconf` package installed: `pip install omegaconf`
*   Familiarity with basic Python syntax and command line

**Lab Setup:**

1.  Create a new directory called `omegaconf_lab`.
2.  Inside `omegaconf_lab`, create the following files:
    *   `config_base.yaml`
    *   `config_override.yaml`
    *   `lab.py`

**Files Content:**

*   **`config_base.yaml`**: This file will contain your base configuration.

    ```yaml
    defaults:
      - experiment_name: "default_experiment"
      - logging: "debug"
      - optimizer: "Adam"
      - learning_rate: 0.001
    
    data:
      batch_size: 32
      num_workers: 4
      dataset: "MNIST"
    
    model:
      architecture: "CNN"
      num_layers: 3
      hidden_size: 64
    
    training:
      epochs: 10
      save_model: True
    ```

*   **`config_override.yaml`**: This file will contain configurations that should override the base.
    ```yaml
    defaults:
      - learning_rate: 0.0005
    data:
      batch_size: 64
    
    model:
      hidden_size: 128
    training:
      epochs: 20
    ```
*   **`lab.py`**: This is your main script where you'll do the work.
    ```python
    from omegaconf import OmegaConf
    import os

    # Load and combine config using OmegaConf.load
    def load_configs():
        #load base config
        base_path = os.path.join(os.path.dirname(__file__), "config_base.yaml")
        base_config = OmegaConf.load(base_path)
        
        #load override config
        override_path = os.path.join(os.path.dirname(__file__), "config_override.yaml")
        override_config = OmegaConf.load(override_path)

        #merge the configs together
        final_config = OmegaConf.merge(base_config, override_config)
        
        return final_config

    # Function to print config values
    def print_config(config, title):
        print("\n" + title)
        print("-" * len(title))
        for key in config:
            print(f"{key}: {config[key]}")
        print("-" * len(title))
        

    def main():
    
        config = load_configs()
        
        #printing all the config to see
        print_config(config, "Merged Configuration:")
        
        #accessing specific values
        print("\nAccessing Specific Values:")
        print(f"  Experiment Name: {config.defaults.experiment_name}")
        print(f"  Dataset: {config.data.dataset}")
        print(f"  Learning Rate: {config.defaults.learning_rate}")
        print(f"  Hidden Size: {config.model.hidden_size}")
        print(f"  Epochs: {config.training.epochs}")
        
        # Modification
        print("\nModifying values:")
        config.data.batch_size = 128 # Set directly
        OmegaConf.set_struct(config, False) # Allow setting new keys
        config.model.dropout_rate = 0.2 # Add a new value
        print(f"  Modified Batch Size: {config.data.batch_size}")
        print(f"  Added Dropout Rate: {config.model.dropout_rate}")
        
        
        #merging more values using from_dotdict
        new_params = {
            "optimizer": "SGD",
            "data.num_workers": 8,
            "training.save_model": False
        }
        config_override_from_dot_dict = OmegaConf.from_dotdict(new_params)
        final_config = OmegaConf.merge(config, config_override_from_dot_dict)
        
        print_config(final_config, "Modified & Merged Configuration:")
        
        #Resolving value (like accessing an environment variable)
        print("\nValue Resolving:")
        OmegaConf.register_new_resolver("get_env_var", lambda x: os.environ.get(x, "not_found"))
        config_resolved = OmegaConf.create({"data": {"output_dir":"${get_env_var:OUTPUT_DIR}"}})
        final_config = OmegaConf.merge(final_config,config_resolved )
        print("Output dir: ", final_config.data.output_dir )
        os.environ["OUTPUT_DIR"] = "my_output_folder"
        config_resolved_after_set = OmegaConf.create({"data": {"output_dir":"${get_env_var:OUTPUT_DIR}"}})
        final_config_resolved_after_set = OmegaConf.merge(final_config, config_resolved_after_set)
        print("Output dir after setting: ", final_config_resolved_after_set.data.output_dir)
        
        # Saving and loading from config.
        saved_config_path = os.path.join(os.path.dirname(__file__), "saved_config.yaml")
        OmegaConf.save(config, saved_config_path)
        loaded_config = OmegaConf.load(saved_config_path)
        print_config(loaded_config, "Loaded Saved Configuration:")
        
    if __name__ == "__main__":
        main()
    ```

**Lab Activities:**

1.  **Load and Merge:** In `lab.py`, implement the `load_configs` function to:
    *   Load `config_base.yaml` using `OmegaConf.load`.
    *   Load `config_override.yaml` using `OmegaConf.load`.
    *   Merge both configurations using `OmegaConf.merge`.
    *  return the new config
2.  **Access Values:** Access and print some of the config values that is returned from the function. (see `lab.py`)
3.  **Modify and Add Values:**
    *   Modify the `batch_size` to `128`.
    *   Add a new value to `model` called `dropout_rate` with a value of `0.2`.
    *   Print the updated value
4. **Merge from dotdict:**
    *   Merge new paramaters to `final_config` using `from_dotdict`. 
    *   Merge: 
        ```python
            {
                "optimizer": "SGD",
                "data.num_workers": 8,
                "training.save_model": False
            }
         ```
    *   Print the modified configuration.
5. **Resolve values:**
    *   Register a resolver for environment variables. 
    *   Add a new variable called `output_dir` using the resolver and set it to a default value. 
    *   Set the `OUTPUT_DIR` environment variable to `my_output_folder`. 
    *   Re-add `output_dir` with the resolver and see the updated value in the config.
6. **Save and Load**:
    *   Save the config to a `saved_config.yaml` file.
    *   Load the config again from the file.
    *   Print the loaded config.

**Grading Criteria:**

*   **Correctness:** Is the config being loaded, merged, and accessed correctly?
*   **Modification:** Are the configs being modified and updated correctly?
*   **Clarity:** Is the code well-organized, easy to read, and properly commented?
*   **Understanding:** Does the code demonstrate understanding of the basic `OmegaConf` concepts?

**Hints:**

*   Use `OmegaConf.load()` to load YAML files.
*   Use `OmegaConf.merge()` to combine configurations.
*   Use dot notation or bracket notation for accessing values (e.g., `config.data.batch_size` or `config['data']['batch_size']`).
*   Use `OmegaConf.set_struct(config, False)` to allow new keys to be added to the config.
*   Use `OmegaConf.save()` to save the config.

**Running the lab:**

1.  Save all files.
2.  Navigate to the `omegaconf_lab` directory in your terminal.
3.  Run `python lab.py`.

This lab should provide a good hands-on experience with `OmegaConf`, making it easier for your students to understand configuration management in their projects. Let me know if you have any other questions.
