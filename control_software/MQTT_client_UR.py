from paho.mqtt import client as mqtt_client

class MQTT_functionality:
    def __init__(self,broker,port):
        __counter = 0
        __counter = __counter + 1
        self.__client_id = str(__counter)
        self.__broker = broker
        self.__port = port
        self.__client = mqtt_client.Client(self.__client_id)

    def connect_mqtt(self) -> mqtt_client:
        #what happens when mqtt connection is established
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.__client.on_connect = on_connect
        self.__client.connect(self.__broker, self.__port)

    def subscribe(self,topic):
        #What happens when message is received(very important)
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        self.__client.on_message = on_message
        self.__client.subscribe(topic)
        self.__client.loop_forever()

    def publish(self,topic,msg):
        msg = f"messages: {msg}"
        result = self.__client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send '{msg}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")




def main():
    test_MQTT_client = MQTT_functionality('192.168.1.246',1883)
    test_MQTT_client.connect_mqtt()
    test_MQTT_client.publish('order/messageCounter','hehehe')
    test_MQTT_client.subscribe('order/messageCounter')

main()
