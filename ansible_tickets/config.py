from yaml import safe_load


class Config:
    __slots__ = ['_conf']

    def __init__(self, filename: str, path: str = '/etc/'):
        """
            Constructor

            :param filename: The name of the config file
            :param path: The path of the config file
        """
        file = f'{path}{filename}'
        with open(file, 'r') as handler:
            self._conf = safe_load(handler)

    def get(self, item: str) -> str:
        """
            Getter for config values

            :param item: The config item required

            :return: Value for config if exists otherwise an empty string
        """
        if item in self._conf:
            return self._conf[item]
        return ''
