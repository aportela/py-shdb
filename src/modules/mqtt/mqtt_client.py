from typing import Optional
import time
import paho.mqtt.client as mqtt

from ...utils.logger import Logger
class MQTTClient():

    def __init__(self, broker: str, port: int = 1883, username: Optional[str] = None, password: Optional[str] = None, topic: Optional[str] = None) -> None:
        self.__log = Logger()

        self.__client = mqtt.Client()

        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message

        if username:
            print(f"Usuario: {username}")
            print(f"Password: {password}")
            self.__client.username_pw_set(username, password)

        if not topic:
            raise ValueError("Topic not set")

        self.__topic = topic
        #self.__client.on_log = self.__on_log

        if not broker:
            raise ValueError("Broker not set")

        self.__client.connect(broker, port, 60)
        self.__client.loop_start()

    def __on_log(self, client, userdata, level, buf):
        self.__log.debug(f"Log: {buf}")

    def __on_connect(self, client, userdata, flags, rc):
        if self.__topic is not None:
            self.__log.info(f"Connected, subscribe to topic {self.__topic}")
            result, _ = client.subscribe(self.__topic)
            if result != mqtt.MQTT_ERR_SUCCESS:
                self.__log.error(f"Failed to subscribe to topic: {self.__topic}")
        else:
            self.__log.info(f"Connected")

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
            if rc == mqtt.MQTT_ERR_CONN_REFUSED:
                raise ValueError(f"Broker disconnected, connection refused")
            else:
                self.__log.info(f"Broker disconnected, auto-reconnecting again")
                self.__reconnect()

    def __on_message(self, client, userdata, msg):
        print("Message received")
        print(f"{msg.topic}: {msg.payload.decode()}")
