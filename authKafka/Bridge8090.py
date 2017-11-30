import paho.mqtt.client as mqtt
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090'])


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, result):
    print("Connected with result code "+str(result))
    client.subscribe("normal.rango1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global producer
    info = json.loads(msg.payload)
    print( "Topic: ", msg.topic+'\nMessage: '+str(msg.payload))
    producer.send('normal.rango1',msg.payload)
    producer.flush()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("rzotnaqy","Nv9nPdbq8Ut-")
client.connect("m14.cloudmqtt.com", 19689, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
