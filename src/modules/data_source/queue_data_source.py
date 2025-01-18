from ...utils.logger import Logger
from ..queue.queue import Queue, QueueMSG

class QueueDataSource:
    def __init__(self) -> None:
        self._log = Logger()
        self.__queue = Queue()

    def _enqueue(self, msg: QueueMSG) -> None:
        self.__queue.enqueue(msg)

    def dequeue(self) -> QueueMSG:
        return self.__queue.dequeue()
