from typing import Any, Optional
from enum import Enum
import re
from decimal import Decimal
from ....utils.logger import Logger
from ...queue.queue import Queue, QueueMSG
from ..mqtt_client import MQTTClient

class MQTTDataSourceValueType(Enum):
    INTEGER = 1
    DECIMAL = 2
    BIG_DECIMAL = 3
    STRING  = 4

class MQTTDataSource:
    def __init__(self, mqtt: MQTTClient, topic: str, extract_pattern: str, extracted_value_type: MQTTDataSourceValueType, search_pattern: Optional[str] = None) -> None:
        self.__log = Logger()
        self.__mqtt = mqtt
        self.__extract_pattern = extract_pattern
        self.__extracted_value_type = extracted_value_type
        if search_pattern is not None:
            self.__search_pattern = search_pattern
            self.__mqtt.add_callback(topic, self.onMQTTTopicMessageWithSearchPattern)
        else:
            self.__mqtt.add_callback(topic, self.onMQTTTopicMessageWithoutSearchPattern)
        self.__queue = Queue()

    def _enqueue(self, msg: QueueMSG) -> None:
        self.__queue.enqueue(msg)

    def _dequeue(self) -> QueueMSG:
        return self.__queue.dequeue()

    def onMQTTTopicMessageWithSearchPattern(self, topic: str, message: str) -> None:
        self.__log.debug(f"Topic: {topic}")
        self.__log.debug(f"Message: {message}")
        found = True
        if self.__search_pattern is not None and not re.search(self.__search_pattern, message):
            found = False
        if (found):
            match = re.search(self.__extract_pattern, message)
            if match:
                self._enqueue(match.group(1))

    def onMQTTTopicMessageWithoutSearchPattern(self, topic: str, message: str) -> None:
        self.__log.debug(f"Topic: {topic}")
        self.__log.debug(f"Message: {message}")
        match = re.search(self.__extract_pattern, message)
        if match:
            if self.__extracted_value_type == MQTTDataSourceValueType.INTEGER:
                self.__queue.enqueue(QueueMSG(int(match.group(1))))
            elif self.__extracted_value_type == MQTTDataSourceValueType.DECIMAL:
                self.__queue.enqueue(QueueMSG(float(match.group(1))))
            elif self.__extracted_value_type == MQTTDataSourceValueType.BIG_DECIMAL:
                self.__queue.enqueue(QueueMSG(Decimal(match.group(1))))
            else:
                self.__queue.enqueue(QueueMSG(match.group(1)))
