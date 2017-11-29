from kafka import KafkaConsumer
import json
import datetime
import sys
import requests
import time
import threading

username = "publisher"
password = "colmines12545"
t = time.time()
# To consume latest messages and auto-commit offsets
print("**Starting publisher")
consumer = KafkaConsumer('bash.' + 'rango1',
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.23:8090'])

i = 0
promedio = 0

print("*started looking for topics to eat*")


class AgregadorThread(threading.Thread):
    def __init__(self, payload):
        threading.Thread.__init__(self)
        self.url = "http://172.24.42.46:8080/mediciones/"
        self.payload = {
            "user": username,
            "pw": password,
            "idMicro": payload['idMicro'],
            "temperatura": payload['temperatura'],
            "sonido": payload['sonido'],
            "gas": payload['gas'],
            "luz": payload['luz'],
            "time": payload['senseTime']
        }

    def setPayload(self, payload):
        self.payload = {
            "user": username,
            "pw": password,
            "idMicro": payload['idMicro'],
            "temperatura": payload['temperatura'],
            "sonido": payload['sonido'],
            "gas": payload['gas'],
            "luz": payload['luz'],
            "time": payload['senseTime']
        }

    def run(self):
        response = requests.post(self.url, data=json.dumps(self.payload), headers={'Content-type': 'application/json'})
        print("Msj:" + str(i) + " Response Status Code: " + str(response.status_code))


class AgregadorConAlerta(AgregadorThread):
    def __init__(self, payload):
        super.__init__(payload)
        self.payload2 = {
            "user": username,
            "pw": password,
            "idMicro": payload['idMicro'],
            "estadoTemp": payload['estadoTemp'],
            "estadoGas": payload['estadoGas'],
            "estadoRuido": payload['estadoRuido'],
            "estadoLuz": payload['estadoLuz']
        }

    def setBigPayload(self, payload):
        super.setPayload(payload)
        self.payload2 = {
            "user": username,
            "pw": password,
            "idMicro": payload['idMicro'],
            "estadoTemp": payload['estadoTemp'],
            "estadoGas": payload['estadoGas'],
            "estadoRuido": payload['estadoRuido'],
            "estadoLuz": payload['estadoLuz']
        }

    def run(self):
        super(AgregadorConAlerta, self).run()
        response = requests.post("http://172.24.42.46:8080/micro/", data=json.dumps(self.payload2),
                                 headers={'Content-type': 'application/json'})
        print("Msj:" + str(i) + " Response Status Code: " + str(response.status_code))


class PoolWrapper(AgregadorConAlerta):
    def __init__(self):
        threading.Thread.__init__(self)
        self.payload = {}
        self.payload2 = {}
        self.event = threading.Event()

    def run(self):
        while True:
            self.event.clear()
            self.event.wait()
            super(PoolWrapper, self).run()


print("creando objetos")

poolSize = 20
pool = []
for i in range(poolSize):
    pool.append(PoolWrapper())
    pool[i].start()
print("Objetos creados en: " + str(time.time() - t) + " s")

for message in consumer:
    print(message)
    try:
        jsonVal = json.loads(message.value)
        if (jsonVal != None and jsonVal['data'] != None):
            valor = int(jsonVal['data'])

            payload = {
                "user": username,
                "pw": password,
                "idMicro": jsonVal['id'],
                "temperatura": int(jsonVal['temperatura']),
                "sonido": int(jsonVal['ruido']),
                "gas": int(jsonVal['gas']),
                "luz": int(jsonVal['luz']),
                "time": jsonVal['senseTime']
            }

            assigned = False
            while not assigned:
                for i in range(poolSize):
                    if not pool[i].event.is_set():
                        pool[i].setBigPayload(payload)
                        pool[i].event.set()
                        assigned = True
                        break
        else:
            print("null value received")
    except:
        print("Error (in)esperado: ", sys.exc_info())
