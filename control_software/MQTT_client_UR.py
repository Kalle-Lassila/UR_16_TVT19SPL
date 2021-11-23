#easy to use MQTT functionality for the whole family

from paho.mqtt import client as mqtt_client
from queue import Queue
from multipledispatch import dispatch

class MQTT_functionality:
    def __init__(self,broker,port):
        self.q1 = Queue(maxsize = 99)
        self.q2 = Queue(maxsize = 99)
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

    @dispatch (str)
    def subscribe(self,topic):
        #What happens when message is received(very important)
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
            self.q1.put(msg.payload.decode())
            #print(self.q1.get())  #TODo This needs to be commented out in the final code otherwise the que will empty here
        self.__client.on_message = on_message
        self.__client.subscribe(topic)
        self.__client.loop_forever()

    @dispatch (str,str)
    def subscribe(self,topicSt,topicNd):
        #What happens when message is received(very important)
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
            if msg.topic == topicSt:
                self.q1.put(msg.payload.decode())
                #print(self.q1.get())  #TODo This needs to be commented out in the final code otherwise the que will empty here
            elif msg.topic == topicNd:
                self.q2.put(msg.payload.decode())
                #print(self.q2.get())  #TODo This needs to be commented out in the final code otherwise the que will empty here
        self.__client.on_message = on_message
        self.__client.subscribe(topicSt)
        self.__client.subscribe(topicNd)
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
    #Initializes the MQTT_functionality object
    #syntax:  xxxxxx = MQTT_functionality('broker name/address',port number)
    test_MQTT_client = MQTT_functionality('192.168.1.246',1883)
    
    #connect to MQTT (should propably be done within the class)
    #TODo move inside the MQTT_functionality Class
    test_MQTT_client.connect_mqtt()

    #publish MQTT messages to desired topic
    #syntax:  xxxxxx.publish('topic name','message')
    test_MQTT_client.publish('order/messageCounter','hehehe')

    #with subscribe method you can subscribe to either one or two topics
    #NOTICE use of this method calls the network loop functions in a infinite loop
    #syntax:  xxxxxx.subscribe('topic name') or xxxxxx.subscribe('first topic name','second topic name')
    test_MQTT_client.subscribe('order/messageCounter','order/messageContents')

main()



