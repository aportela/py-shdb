from typing import Optional, Any
from ...utils.logger import Logger
import time
import queue

class QueueMSG:
    def __init__(self, value: Any, timestamp: Optional[float] = None):
        self.value = value
        if timestamp is not None:
            self.timestamp = timestamp
        else:
            self.timestamp = time.time()

class Queue:
    def __init__(self):
        self.__log = Logger()
        self.__shared_queue = queue.Queue()

    def enqueue(self, msg: QueueMSG):
        self.__log.debug(f"enqueue message: {msg.value} - timestamp: {msg.timestamp}")
        self.__shared_queue.put(msg)

    def dequeue(self) -> Optional[QueueMSG]:
        try:
            msg = self.__shared_queue.get_nowait()
            self.__log.debug(f"dequeue message: {msg}")
            return msg
        except queue.Empty:
            self.__log.debug("empty queue")
            #time.sleep(0.2)
            return None
