import json

def load_config(config_path):
    """
    Load job titles, locations, and country settings from an external config.json file.

    Args:
        config_path (str): Path to the configuration JSON file.

    Returns:
        dict: A dictionary containing job titles, locations, and country_indeed.
    Raises:
        FileNotFoundError: If the config file is not found.
        ValueError: If the config format is invalid.
    """
    try:
        with open(config_path, "r") as file:
            config = json.load(file)

            # Validate required keys
            if not all(key in config for key in ["job_titles", "locations", "country_indeed"]):
                raise ValueError(f"{config_path} is missing one or more required keys: 'job_titles', 'locations', 'country_indeed'.")

            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"{config_path} not found. Please provide the correct path.")
    except json.JSONDecodeError:
        raise ValueError(f"{config_path} contains invalid JSON.")
