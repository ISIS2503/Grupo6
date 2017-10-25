import json
import threading


from kafka import KafkaConsumer

import States

totalSensores=2500
numeroRangos=1

micros=[]

##valores variables
rango=1



# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.'+'rango'+str(rango),group_id='my-group',bootstrap_servers=['172.24.42.23:8090'])
sem= threading.BoundedSemaphore()
promedio = 1
valorPrueba = 1500
i=0

class AgregadorThread(threading.Thread):

    global promedio
    global i
    def __init__(self,id,temperatura,gas,ruido,luz,time):
        self.id=id
        self.temperatura=temperatura
        self.gas=gas
        self.ruido=ruido
        self.luz=luz
        self.time=time
    def run(self):
        micros[self.id].agregarTemperatura(self.temperatura)
        micros[self.id].agregarGas(self.gas)
        micros[self.id].agregarRuido(self.ruido)
        micros[self.id].agregarLuz(self.luz)
        sem.acquire()
        self.promedio= (self.time-time.time()+self.promedio*self.i)/(self.i+1)
        sem.release()
        sem.notify()





init=totalSensores/numeroRangos*(rango-1)
for i in range(int(totalSensores/numeroRangos)):
    micros.append(States.Sensor(init+i))

for message in consumer:
    print(message)
    jsonVal=json.loads(message.value)
    id=jsonVal['id']
    temperatura=jsonVal['temperatura']
    gas=jsonVal['gas']
    ruido=jsonVal['ruido']
    luz=jsonVal['luz']
    time=jsonVal['time']
    a=AgregadorThread(id,temperatura,gas,ruido,luz,time)
    a.start()
    sem.acquire()
    while(i<valorPrueba):
        sem.wait()
    print(str(i)+" :"+ str(promedio))





