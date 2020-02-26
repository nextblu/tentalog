import os
import logging.config
import logging
import coloredlogs
import yaml

try:
    from importlib import resources as res
except ImportError:
    import importlib_resources as res


def setup_logging(path="default_logging.yaml", level=logging.INFO):
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print("Error in Logging Configuration. Using default configuration")
                print(e)
                logging.basicConfig(level=level)
                coloredlogs.install(level=level)
    else:
        # file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_logging.yaml")
        file_path = os.path.join(os.path.dirname(__file__), "default_configuration.yaml")
        print(file_path)
        with open(file_path) as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception as e:
                print("Error in Logging Configuration. Using default configuration")
                print(e)
                logging.basicConfig(level=level)
                coloredlogs.install(level=level)
