"""Module to handle configuration."""
from yaml import safe_load


class Config:
    """Class to handle configuration."""

    __slots__ = ["_conf"]

    def __init__(self, filename: str, path: str = "/etc/"):
        """
        Initialise Config.

        :param filename: The name of the config file
        :param path: The path of the config file
        """
        file = f"{path}{filename}"
        with open(file, "r") as handler:
            self._conf = safe_load(handler)

    def get(self, item: str) -> str:
        """
        Getter for config values.

        :param item: The config item required

        :return: Value for config if exists otherwise an empty string
        """
        return self._conf[item] if item in self._conf else ""
