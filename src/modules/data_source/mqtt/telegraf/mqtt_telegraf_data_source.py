from typing import Optional
import re
from decimal import Decimal
from ...mqtt.mqtt_data_source import MQTTDataSource
from ....mqtt.mqtt_client import MQTTClient
from ....queue.queue import QueueMSG

# TODO: refactor MQTTTelegrafCPULoadDataSource
class MQTTTelegrafCPUDataSource (MQTTDataSource):
    def __init__(self, mqtt: MQTTClient, topic: str) -> None:
        super().__init__(mqtt = mqtt, topic = topic)

    def _parse(self, topic: str, message: str, timestamp: Optional[float] = None):
        #self._log.debug(message)
        if re.search(r"usage_idle=", message):
            #usage_user = self._extract_decimal(pattern = r"usage_user=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_system = self._extract_decimal(pattern = r"usage_system=([0-9]+(?:\.[0-9]+)?)", message = message)
            usage_idle = self._extract_big_decimal(pattern = r"usage_idle=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_active = self._extract_decimal(pattern = r"usage_active=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_nice = self._extract_decimal(pattern = r"usage_nice=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_iowait = self._extract_decimal(pattern = r"usage_iowait=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_irq = self._extract_decimal(pattern = r"usage_irq=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_softirq = self._extract_decimal(pattern = r"usage_softirq=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_steal = self._extract_decimal(pattern = r"usage_steal=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_guest = self._extract_decimal(pattern = r"usage_guest=([0-9]+(?:\.[0-9]+)?)", message = message)
            #usage_guest_nice = self._extract_decimal(pattern = r"usage_guest_nice=([0-9]+(?:\.[0-9]+)?)", message = message)
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
            temp = self._extract_decimal(pattern = r"temp_input=([0-9]+(?:\.[0-9]+)?)", message = message)
        # TODO: not working with raspberry PI feature=temp1
        #if temp is None:
            #temp = self._extract_decimal(pattern = r"temp=([0-9]+(?:\.[0-9]+)?)", message = message)
        if temp is not None:
            self._enqueue(QueueMSG(value = temp, timestamp = timestamp))

class MQTTTelegrafMemoryDataSource (MQTTDataSource):
    def __init__(self, mqtt: MQTTClient, topic: str) -> None:
        super().__init__(mqtt = mqtt, topic = topic)

    def _parse(self, topic: str, message: str, timestamp: Optional[float] = None):
        #self._log.debug(message)
        #active = self._extract_integer(pattern = r"active=([0-9]+)", message = message)
        #available = self._extract_integer(pattern = r"available=([0-9]+)", message = message)
        #available_percent = self._extract_decimal(pattern = r"available_percent=([0-9]+(?:\.[0-9]+)?)", message = message)
        #buffered = self._extract_integer(pattern = r"buffered=([0-9]+)", message = message)
        #cached = self._extract_integer(pattern = r"cached=([0-9]+)", message = message)
        #commit_limit = self._extract_integer(pattern = r"commit_limit=([0-9]+)", message = message)
        #committed_as = self._extract_integer(pattern = r"committed_as=([0-9]+)", message = message)
        #dirty = self._extract_integer(pattern = r"dirty=([0-9]+)", message = message)
        #free = self._extract_integer(pattern = r"free=([0-9]+)", message = message)
        #high_free = self._extract_integer(pattern = r"high_free=([0-9]+)", message = message)
        #high_total = self._extract_integer(pattern = r"high_total=([0-9]+)", message = message)
        #huge_pages_free = self._extract_integer(pattern = r"huge_pages_free=([0-9]+)", message = message)
        #huge_page_size = self._extract_integer(pattern = r"huge_page_size=([0-9]+)", message = message)
        #huge_pages_total = self._extract_integer(pattern = r"huge_pages_total=([0-9]+)", message = message)
        #inactive = self._extract_integer(pattern = r"inactive=([0-9]+)", message = message)
        #laundry = self._extract_integer(pattern = r"laundry=([0-9]+)", message = message)
        #low_free = self._extract_integer(pattern = r"low_free=([0-9]+)", message = message)
        #low_total = self._extract_integer(pattern = r"low_total=([0-9]+)", message = message)
        #mapped = self._extract_integer(pattern = r"mapped=([0-9]+)", message = message)
        #page_tables = self._extract_integer(pattern = r"page_tables=([0-9]+)", message = message)
        #shared = self._extract_integer(pattern = r"shared=([0-9]+)", message = message)
        #slab = self._extract_integer(pattern = r"slab=([0-9]+)", message = message)
        #sreclaimable = self._extract_integer(pattern = r"sreclaimable=([0-9]+)", message = message)
        #sunreclaim = self._extract_integer(pattern = r"sunreclaim=([0-9]+)", message = message)
        #swap_cached = self._extract_integer(pattern = r"swap_cached=([0-9]+)", message = message)
        #swap_free = self._extract_integer(pattern = r"swap_free=([0-9]+)", message = message)
        #swap_total = self._extract_integer(pattern = r"swap_total=([0-9]+)", message = message)
        #total = self._extract_integer(pattern = r"total=([0-9]+)", message = message)
        #used = self._extract_integer(pattern = r"used=([0-9]+)", message = message)
        used_percent = self._extract_decimal(pattern = r"used_percent=([0-9]+(?:\.[0-9]+)?)", message = message)
        #vmalloc_chunk = self._extract_integer(pattern = r"vmalloc_chunk=([0-9]+)", message = message)
        #vmalloc_total = self._extract_integer(pattern = r"vmalloc_total=([0-9]+)", message = message)
        #vmalloc_used = self._extract_integer(pattern = r"vmalloc_used=([0-9]+)", message = message)
        #wired = self._extract_integer(pattern = r"wired=([0-9]+)", message = message)
        #write_back = self._extract_integer(pattern = r"write_back=([0-9]+)", message = message)
        #write_back_tmp = self._extract_integer(pattern = r"write_back_tmp=([0-9]+)", message = message)
        if used_percent is not None:
            self._enqueue(QueueMSG(value = used_percent, timestamp = timestamp))
