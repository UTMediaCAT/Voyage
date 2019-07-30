import yaml
import os

conf = None
def get_config():
    """ (None) -> dict
    Returns a dictionary containing the micro settings from the
    config.yaml file located in the directory containing this file
    """
    global conf
    if(conf is None):
        path = os.path.abspath(os.path.join(__file__, "..", "..", "..", "config.yaml"))
        config_yaml = open(path, 'r')

        conf = yaml.load(config_yaml)
        config_yaml.close()
    return conf