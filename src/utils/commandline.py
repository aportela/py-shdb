import sys
import argparse
from typing import Optional
from .logger import Logger

class Commandline:

    def __init__(self):
        self.__logger = Logger()
        self.__logger.debug(f"Commandline args: {sys.argv}")
        parser = argparse.ArgumentParser()
        parser.add_argument('-config', type=str, help='Path to configuration file.', required=False)
        parser.add_argument('-skin', type=str, help='Path to skin configuration file.', required=False)
        self.__args = parser.parse_args()

    @property
    def configuration(self) -> Optional[str]:
        return self.__args.config

    @property
    def skin(self) -> Optional[str]:
        return self.__args.skin
