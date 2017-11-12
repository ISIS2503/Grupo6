import paho.mqtt.client as mqtt
import json
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='172.24.42.23:8091',
                          security_protocol='SSL',
                          ssl_check_hostname=True,
                          ssl_cafile='CARoot.pem',
                          ssl_certfile='certificate.pem',
                          ssl_keyfile='key.pem')
#producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8091'],
 #                        security_protocol='SSL')
                         #ssl_certfile = './authKafka/cert-file',
                         #ssl_keyfile = './authKafka/ca-key')
                         #ssl_password = 'Isis2503.')
                         #ssl_keystore_location = './authKafka/kafka.server.keystore.jks',
                         #ssl_keystore_password = 'Isis2503.',
                         #ssl_truststore_location = './authKafka/kafka.server.truststore.jks',
                         #ssl_truststore_password = 'Isis2503.')
                         #ssl_keystore_type = 'JKS',
                         #ssl_truststore_type = 'JKS')
                         #sasl_mechanism='PLAIN',
                         #sasl_plain_username='admin',
                         #sasl_plain_password='admin')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc, result):
    print("Connected with result code "+str(result))
    client.subscribe("normal.rango2")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global producer
    info = json.loads(msg.payload)
    print( "Topic: ", msg.topic+'\nMessage: '+str(msg.payload))
    producer.send('normal.rango2',msg.payload)
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
