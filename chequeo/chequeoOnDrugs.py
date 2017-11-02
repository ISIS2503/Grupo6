import json
import threading
import time


from kafka import KafkaConsumer

import States

totalSensores=2500
numeroRangos=1

micros=[]

##valores variables
rango=1



# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.'+'rango'+str(rango),group_id='my-group',bootstrap_servers=['172.24.42.46:8090'])
sem= threading.BoundedSemaphore()
promedio = 1
valorPrueba = 1500
i=0

class AgregadorThread(threading.Thread):
	def __init__(self,id,temperatura,gas,ruido,luz,time):
		threading.Thread.__init__(self)
		self.id=id
		self.temperatura=temperatura
		self.gas=gas
		self.ruido=ruido
		self.luz=luz
		self.time=time
	def run(self):
		global promedio
		global i
		micros[self.id].agregarTemperatura(self.temperatura)
		micros[self.id].agregarGas(self.gas)
		micros[self.id].agregarRuido(self.ruido)
		micros[self.id].agregarLuz(self.luz)
		sem.acquire()
		promedio= (self.time-time.time()+promedio*i)/(i+1)
		sem.release()
		sem.notify()

def chequearConexion():
	for micro in micros:
		ya = time.time()
		if (ya - micro.tiempoGas >= 300):
			micro.goState(micro.estadoGas, 0, 350, "")
		if (ya - micro.tiempoRuido >= 300):
			micro.goState(micro.estadoRuido, 0, 350, "")
		if (ya - micro.tiempoLuz >= 300):
			micro.goState(micro.estadoLuz, 0, 350, "")
		if (ya - micro.tiempoTemperatura >= 300):
			micro.goState(micro.estadoTemperatura, 0, 350, "")

	threading.Timer(300.0, chequearConexion).start()



#init=totalSensores/numeroRangos*(rango-1)
init=0
print("creando objetos")
t=time.time()
for i in range(totalSensores):
	micros.append(States.Sensor(init+i))
	print(i)
print("Objetos creados tiempo tomado: "+str(time.time()-t))
chequearConexion()
for message in consumer:
    print(message)
    jsonVal=json.loads(message.value)
    id=int(jsonVal['id'])
    temperatura=int(jsonVal['temperatura'])
    gas=int(jsonVal['gas'])
    ruido=int(jsonVal['ruido'])
    luz=int(jsonVal['luz'])
    time=int(jsonVal['sensetime'])
    a=AgregadorThread(id,temperatura,gas,ruido,luz,time)
    a.start()
    sem.acquire()
while i<valorPrueba :
	sem.release()
	time.sleep(1)
	sem.acquire()
print(str(i)+" :"+ str(promedio))





