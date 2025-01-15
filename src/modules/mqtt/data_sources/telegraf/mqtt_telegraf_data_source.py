from typing import Optional
import re
from decimal import Decimal
from ..mqtt_data_source import MQTTDataSource
from ...mqtt_client import MQTTClient
from ....queue.queue import QueueMSG

# TODO: refactor MQTTTelegrafCPULoadDataSource
class MQTTTelegrafCPUDataSource (MQTTDataSource):
    def __init__(self, mqtt: MQTTClient, topic: str) -> None:
        super().__init__(mqtt = mqtt, topic = topic)

    def _parse(self, topic: str, message: str, timestamp: Optional[float] = None):
        #self._log.debug(message)
        if re.search(r"usage_idle=", message):
            #usage_user = self._extract_big_decimal(pattern = r"usage_user=([0-9]+\.[0-9]+)", message = message)
            #usage_system = self._extract_big_decimal(pattern = r"usage_system=([0-9]+\.[0-9]+)", message = message)
            usage_idle = self._extract_big_decimal(pattern = r"usage_idle=([0-9]+\.[0-9]+)", message = message)
            #usage_active = self._extract_big_decimal(pattern = r"usage_active=([0-9]+\.[0-9]+)", message = message)
            #usage_nice = self._extract_big_decimal(pattern = r"usage_nice=([0-9]+\.[0-9]+)", message = message)
            #usage_iowait = self._extract_big_decimal(pattern = r"usage_iowait=([0-9]+\.[0-9]+)", message = message)
            #usage_irq = self._extract_big_decimal(pattern = r"usage_irq=([0-9]+\.[0-9]+)", message = message)
            #usage_softirq = self._extract_big_decimal(pattern = r"usage_softirq=([0-9]+\.[0-9]+)", message = message)
            #usage_steal = self._extract_big_decimal(pattern = r"usage_steal=([0-9]+\.[0-9]+)", message = message)
            #usage_guest = self._extract_big_decimal(pattern = r"usage_guest=([0-9]+\.[0-9]+)", message = message)
            #usage_guest_nice = self._extract_big_decimal(pattern = r"usage_guest_nice=([0-9]+\.[0-9]+)", message = message)
            if usage_idle is not None:
                if usage_idle <= 100.0:
                    self._enqueue(QueueMSG(value = Decimal(100.0) - usage_idle, timestamp = timestamp))
                else:
                    self._enqueue(QueueMSG(value = 0.0, timestamp = timestamp))

class MQTTTelegrafCPUTemperatureDataSource (MQTTDataSource):
    def __init__(self, mqtt: MQTTClient, topic: str) -> None:
        super().__init__(mqtt = mqtt, topic = topic)

    def _parse(self, topic: str, message: str, timestamp: Optional[float] = None):
        #self._log.debug(message)
        temp = None
        if re.search(r"feature=package_id_0", message):
            #usage_user = self._extract_big_decimal(pattern = r"usage_user=([0-9]+\.[0-9]+)", message = message)
            #usage_system = self._extract_big_decimal(pattern = r"usage_system=([0-9]+\.[0-9]+)", message = message)
            temp = self._extract_decimal(pattern = r"temp_input=([0-9]+\.[0-9]+)", message = message)
            #usage_active = self._extract_big_decimal(pattern = r"usage_active=([0-9]+\.[0-9]+)", message = message)
            #usage_nice = self._extract_big_decimal(pattern = r"usage_nice=([0-9]+\.[0-9]+)", message = message)
            #usage_iowait = self._extract_big_decimal(pattern = r"usage_iowait=([0-9]+\.[0-9]+)", message = message)
            #usage_irq = self._extract_big_decimal(pattern = r"usage_irq=([0-9]+\.[0-9]+)", message = message)
            #usage_softirq = self._extract_big_decimal(pattern = r"usage_softirq=([0-9]+\.[0-9]+)", message = message)
            #usage_steal = self._extract_big_decimal(pattern = r"usage_steal=([0-9]+\.[0-9]+)", message = message)
            #usage_guest = self._extract_big_decimal(pattern = r"usage_guest=([0-9]+\.[0-9]+)", message = message)
            #usage_guest_nice = self._extract_big_decimal(pattern = r"usage_guest_nice=([0-9]+\.[0-9]+)", message = message)
        else:
            temp = self._extract_decimal(pattern = r"temp=([0-9]+\.[0-9]+)", message = message)
        if temp is not None:
            self._enqueue(QueueMSG(value = temp, timestamp = timestamp))
