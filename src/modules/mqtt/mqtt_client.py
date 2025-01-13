from typing import Optional, Callable, Dict, List
import paho.mqtt.client as mqtt
import time
from ...utils.logger import Logger

class MQTTClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Singleton: ensures a unique instance of MQTTClient.
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

        # Assign MQTT client event handlers
        self.__client.on_connect = self.__on_connect
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.on_message = self.__on_message

        if username:
            self.__client.username_pw_set(username, password)

        self.__callbacks: Dict[str, List[Callable[[str, str], None]]] = {}

        try:
            self.__client.connect(broker, port, 60)
            self.__client.loop_start()
        except Exception as e:
            self.__log.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def __on_connect(self, client, userdata, flags, rc):
        """
        Handles the MQTT broker connection event.
        """
        if rc == 0:
            self.__log.info("Connected to the broker.")
        else:
            self.__log.warning(f"Error while connecting to broker. Error code: {rc}")

    def __on_disconnect(self, client, userdata, rc):
        """
        Handles the MQTT broker disconnection event.
        """
        self.__log.warning("Broker disconnected.")
        if rc != 0:  # Reconnect if the disconnection was not intentional
            self.__log.info("Attempting to reconnect...")
            self.__reconnect()

    def __reconnect(self):
        """
        Attempts to reconnect to the MQTT broker.
        """
        while True:
            try:
                self.__client.reconnect()
                self.__log.info("Reconnected successfully.")
                break
            except mqtt.MQTTException as e:
                self.__log.warning(f"Reconnection attempt failed: {e}")
                time.sleep(5)

    def __on_message(self, client, userdata, msg):
        """
        Handles incoming messages and triggers registered callbacks for the corresponding topic.
        """
        payload = msg.payload.decode()
        for topic, callbacks in self.__callbacks.items():
            if mqtt.topic_matches_sub(topic, msg.topic):
                for callback in callbacks:
                    try:
                        callback(msg.topic, payload)
                    except Exception as e:
                        self.__log.error(f"Error in callback for topic {msg.topic}: {e}")

    def add_callback(self, topic: str, callback: Callable[[str, str], None]):
        """
        Registers a callback function for a specific topic.
        :param topic: The topic to subscribe to.
        :param callback: The function to execute when a message is received on the topic.
        """
        if topic not in self.__callbacks:
            self.__callbacks[topic] = []
            self.__log.info(f"Subscribing to topic: {topic}.")
            self.__client.subscribe(topic)
        self.__callbacks[topic].append(callback)
        self.__log.info(f"Callback registered for topic: {topic}")

    def remove_callback(self, topic: str, callback: Callable[[str, str], None]):
        """
        Removes a specific callback for a topic.
        :param topic: The topic associated with the callback.
        :param callback: The callback function to remove.
        """
        if topic in self.__callbacks and callback in self.__callbacks[topic]:
            self.__callbacks[topic].remove(callback)
            self.__log.info(f"Callback removed for topic: {topic}.")
            if not self.__callbacks[topic]:
                self.__client.unsubscribe(topic)
                del self.__callbacks[topic]
                self.__log.info(f"Unsubscribed from topic: {topic}.")
