import yaml

class Configuration:
    def __init__(self, path):
        with open(path) as config_file:
            self._config = yaml.load(config_file)

    @property
    def replies(self):
        return self._config['replies']

