from kafka import KafkaConsumer
import time
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import threading
import datetime


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.'+'*',
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.46:8090'])

    

for message in consumer:
    jsonVal=json.loads(message.value)
    if (jsonVal!= None and jsonVal['data']!=None):
        valor=int(jsonVal['data'])
        id=int(jsonVal['idSensor'])
        time=jsonVal['time']
        
        url = 'http://localhost:8080/sensors/' 
        payload={
      'idSensor': id,
      'time': datetime.datetime.now(),
      'valor': valor
      }
	response = requests.post(url, data=json.dumps(payload),
							 headers={'Content-type': 'application/json'})
	print(message.topic)
	print("Response Status Code: " + str(response.status_code))
    ## caso en el que el valor recibido esta mal formado
    else:
        print("null value received")

        
