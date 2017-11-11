import paho.mqtt.client as mqtt
import json
from kafka import KafkaProducer

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, result):
    #print("Connected with result code "+str(result))
    client.subscribe("test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    info = json.loads(msg.payload)
    #print( "Topic: ", msg.topic+'\nMessage: '+str(info))
    producer.send('normal.rango2',bstr(info))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("rzotnaqy","Nv9nPdbq8Ut-")
client.connect("m14.cloudmqtt.com", 19689, 60)

producer = KafkaProducer(bootstrap_servers='localhost:8085',
                         security_protocol="SASL_PLAINTEXT",
                         sasl_mechanism='PLAIN',
                         sasl_plain_username='admin',
                         sasl_plain_password='admin')

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()