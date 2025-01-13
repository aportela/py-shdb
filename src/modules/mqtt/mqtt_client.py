from typing import Optional, Callable, Dict, List
import paho.mqtt.client as mqtt
import time
from ...utils.logger import Logger

class MQTTClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton: ensures unique instance of MQTTClient
        """
        if cls._instance is None:
            cls._instance = super(MQTTClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, broker: str, port: int = 1883, username: Optional[str] = None,
                 password: Optional[str] = None) -> None:
        if hasattr(self, "_initialized"):
            return
        self._initialized = True

        self.__log = Logger()
        self.__client = mqtt.Client()

        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message

        if username:
            self.__client.username_pw_set(username, password)

        self.__callbacks: Dict[str, List[Callable[[str, str], None]]] = {}

        self.__client.connect(broker, port, 60)
        self.__client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        """
        MQTT broker on connect event
        """
        if rc == 0:
            self.__log.info(f"Connected to broker.")
        else:
            self.__log.warning(f"Error while connecting to broker. ErrorCode: {rc}")

    def __on_disconnect(self, client, userdata, rc):
        """
        MQTT broker on disconnect event
        """
        self.__log.warning("Broker disconnected.")
        if rc != 0:  # re-connect if disconection was not intentional
            self.__log.info("Trying re-connect...")
            self.__reconnect()

    def __reconnect(self):
        """
        re-connect to MQTT broker if disconnected
        """
        while True:
            try:
                self.__client.reconnect()
                self.__log.info("Re-connect successful.")
                break
            except Exception as e:
                self.__log.warning(f"Error while re-connecting: {e}")
                time.sleep(5)

    def __on_message(self, client, userdata, msg):
        """
        MQTT broker on message event
        Calls registered callbacks for corresponding topic
        """
        payload = msg.payload.decode()
        #self.__log.info(f"Received message on {msg.topic}: {payload}")
        for topic, callbacks in self.__callbacks.items():
            if mqtt.topic_matches_sub(topic, msg.topic):
                for callback in callbacks:
                    callback(msg.topic, payload)

    def add_callback(self, topic: str, callback: Callable[[str, str], None]):
        """
        Registers callback for specific topic
        :param topic: associated topic
        :param callback: function to execute if message is received on topic
        """
        if topic not in self.__callbacks:
            self.__callbacks[topic] = []
            self.__log.info(f"Subscribe to the topic {topic}.")
            self.__client.subscribe(topic)
        self.__callbacks[topic].append(callback)
        self.__log.info(f"Callback registered for topic: {topic}")
