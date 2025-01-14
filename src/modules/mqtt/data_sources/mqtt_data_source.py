from typing import Optional
from abc import abstractmethod
import re
from decimal import Decimal
from ....utils.logger import Logger
from ...queue.queue import Queue, QueueMSG
from ..mqtt_client import MQTTClient


class MQTTDataSource:
    def __init__(self, mqtt: MQTTClient, topic: str) -> None: #), extract_pattern: str, extracted_value_type: MQTTDataSourceValueType, search_pattern: Optional[str] = None) -> None:
        self._log = Logger()
        self.__mqtt = mqtt
        self.__queue = Queue()
        self.__mqtt.add_callback(topic = topic, callback = self.__on_message_received)

    def _enqueue(self, msg: QueueMSG) -> None:
        self.__queue.enqueue(msg)

    def _dequeue(self) -> QueueMSG:
        return self.__queue.dequeue()

    def __on_message_received(self, topic: str, message: str) -> None:
        self._parse(topic = topic, message = message, timestamp = self.__extract__timestamp(message=message))

    @abstractmethod
    def _parse(self, topic: str, message: str, timestamp: Optional[float] = None):
        pass

    def __extract__timestamp(self, message: str) -> Optional[float]:
        match = re.search(r"(\d+)$", message)
        if match:
            return float(int(match.group(1)) / 1e9)
        else:
            return None

    def _extract_integer(self, pattern: str, message: str) -> Optional[int]:
        match = re.search(pattern, message)
        if match:
            return int(match.group(1))
        else:
            return None

    def _extract_decimal(self, pattern: str, message: str) -> Optional[float]:
        match = re.search(pattern, message)
        if match:
            return float(match.group(1))
        else:
            return None

    def _extract_big_decimal(self, pattern: str, message: str) -> Optional[Decimal]:
        match = re.search(pattern, message)
        if match:
            return Decimal(match.group(1))
        else:
            return None
