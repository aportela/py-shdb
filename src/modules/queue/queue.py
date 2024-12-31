from typing import Optional
#import time
from ...utils.logger import Logger

import queue

class QueueMSG:
    def __init__(self):
        self.__value = None

class Queue:
    def __init__(self):
        self.__log = Logger()
        self.__shared_queue = queue.Queue()

    def enqueue(self, msg: QueueMSG):
        self.__log.debug("enqueue message: {msg}")
        self.__shared_queue.put(msg)

    def dequeue(self) -> Optional[QueueMSG]:
        try:
            msg = self.__shared_queue.get_nowait()
            self.__log.debug("dequeue message: {msg}")
            return msg
        except queue.Empty:
            self.__log.debug("empty queue")
            #time.sleep(0.2)
            return None
