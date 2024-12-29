import time
import paho.mqtt.client as mqtt

from ...utils.logger import Logger
class MQTTClient():

    def __init__(self, broker: str, port: int = 1883, topic: str = "topic_test") -> None:
        self.__log = Logger()

        self.__client = mqtt.Client()

        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message

        self.__client.connect(broker, port, 60)
        self.__client.loop_start()

        self.__topic = topic

    def __on_connect(self, client, userdata, flags, rc):
        if self.__topic is not None:
            client.subscribe(self.__topic)

    def __reconnect(self):
        while True:
            try:
                self.__client.reconnect()
                self.__log.info(f"Reconnect successfull")
                break
            except Exception as e:
                self.__log.warning(f"Error while reconnecting: {e}")
                time.sleep(5)

    def __on_disconnect(self, client, userdata, rc):
        if rc != 0:  # reconnect if disconnection was not forced
            self.__log.info(f"Broker disconnected, auto-reconnecting again")
            self.__reconnect()

    def __on_message(self, client, userdata, msg):
        print(f"{msg.topic}: {msg.payload.decode()}")
