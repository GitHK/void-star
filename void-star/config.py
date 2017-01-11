import yaml


def load_config(config_file_path):
    try:
        with open(config_file_path, 'r') as config_file:
            return yaml.load(config_file)
    except IOError:
        raise IOError("Cannot open configuration file")
