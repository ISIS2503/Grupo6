from kafka import KafkaConsumer
import json
import datetime
import sys
import requests
import time

t=time.time()
# To consume latest messages and auto-commit offsets
print("**Starting publisher")
consumer = KafkaConsumer('normal.'+'rango1',
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.46:8090'])


print("*started looking for topics to eat*")
for message in consumer:
    print(message)
    try:
        jsonVal=json.loads(message.value)
        if (jsonVal!= None and jsonVal['data']!=None):
            valor=int(jsonVal['data'])
            id=int(jsonVal['idSensor'])
            url = "http://localhost:8000/sensores/"
            payload={
                "idSensor": id,
                "time": str(datetime.datetime.now()).split(" ")[1],
               # "time": str(int(datetime.time(time.time()-t))),
                "valor": valor
          }

            print(json.dumps(payload))
            response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
            print(message.topic)
            print("Response Status Code: " + str(response.status_code))
        ## caso en el que el valor recibido esta mal formado
        else:
            print("null value received")

    except:
        print("Error (in)esperado: ",sys.exc_info())
