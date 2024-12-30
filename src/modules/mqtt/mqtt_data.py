from typing import Any, Optional
from abc import abstractmethod
import time
from ...utils.logger import Logger
from ..queue.queue import Queue, QueueMSG
from mqtt_client import MQTTClient
import re

class MQTTData:
    def __init__(self, mqtt: MQTTClient, topic: str, pattern: str) -> None:
        self._log = Logger()
        self.__mqtt = mqtt
        self.__queue = Queue()
        self.__topic = topic
        # TODO: set handler for topic messages
        self.__pattern = pattern

    def onMQTTTopicMessage(self, message: str) -> None:
        #re.search(self.__pattern, message)
        #self.__queue.enqueue(message)
        pass
