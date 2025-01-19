import threading
import math
import random
import time
from ..queue_data_source import QueueDataSource
from ...queue.queue import QueueMSG

class RandomDataSource (QueueDataSource):
    def __init__(self, interval: float = 1) -> None:
        super().__init__()
        self._running = True
        self._thread = None
        self.current_time = 0.0
        self.__interval = interval
        self._start_auto_enqueue()

    def __del__(self):
        self.stop()

    def _get_random(self) -> float:
        self.current_time += 0.1
        load = (
            50
            + 30 * math.sin(self.current_time)
            + 20 * math.sin(self.current_time * 0.5)
        )
        load += random.uniform(-5, 5)
        return max(0.0, min(100.0, load))


    def _start_auto_enqueue(self) -> None:
        def auto_enqueue():
            while self._running:
                self._enqueue(QueueMSG(value = self._get_random(), timestamp = time.time()))
                time.sleep(self.__interval)
        self._thread = threading.Thread(target = auto_enqueue, daemon = True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        self._thread.join()
        self._log.info("Auto-enqueue stopped.")