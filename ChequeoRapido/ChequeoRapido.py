from kafka import KafkaConsumer
import time
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
import threading
import requests

totalSensores=10000
numeroRangos=8

##valores variables
rango=1
##

valores=[]
tiempos=[]
perdidos=[]
inic=time.time()
for i in range(int(totalSensores/numeroRangos)):
    valores.append([])
    tiempos.append(inic)
    perdidos.append(0)

producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090'], value_serializer=lambda m: json.dumps(m).encode('ascii'))


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.'+'rango'+str(rango),
                         group_id='my-group',
                         bootstrap_servers=['172.24.42.23:8090'])
i=1;
promedio=0
temperature=0

##este metodo es llamado cada 5 min y hace un chequeo de los ultimos tiempos de recepcion de los sensores

def busquedaPerdidos():
    #distinccion de casos
    #0 es temperatura
    #1 es luz
    #2 ruido
    #3 gases
    for  temp in range(len(tiempos)) :
        if(temp%4==0 or temp%4==3):
            if time.time()-tiempos[temp]>300:     
                print("sensor fuera de linea")
                idSensor = str(temp+(rango-1)*totalSensores/numeroRangos)
                producer.send('alta.fueradelinea', {'idSensor': idSensor})
                postAlerta(idSensor, "Fuera de linea")
        else:
            ##caso de gases y ruido
            if time.time()-tiempos[temp]>600: 
                print("sensor fuera de linea")
                idSensor = str(temp+(rango-1)*totalSensores/numeroRangos)    
                producer.send('alta.fueradelinea', {'idSensor': idSensor})
                postAlerta(idSensor, "Fuera de linea")


                    
    
    threading.Timer(300.0,busquedaPerdidos).start()
    
def postAlerta(idSensor, tipoAlerta):
    print("enviando alerta: "+ tipoAlerta + "...")
    url="http://localhost:8000/alertas/"
    payload = {
        "idSensor" : idSensor,
        "timeStamp" : str(time.time()),
        "tipoAlerta" : tipoAlerta
    }
    response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    print(str(idSensor) + " Tipo Alerta: "+tipoAlerta+ " Response Status code: " + str(response.status.code))
##llamar la funcion    
busquedaPerdidos()

for message in consumer:
    alerta=0   

    jsonVal=json.loads(message.value)
    if (jsonVal!= None and jsonVal['temperature']!=None):
        jsonDataVal = jsonVal['temperature']
        print(jsonDataVal)
        valor=int(jsonDataVal['data'])
        id=int(jsonDataVal['idSensor'])
        tipo=id%4 
        if (len(valores[id])!=10):
            valores[id].append(valor)
            promedio=valor
        else:
            valores[id].pop(0)
            valores[id].append(valor)
            promedio=sum(valores[id])/10#separacion de casos para dictar la alerta    
            if(tipo==0): #temperatura
                if promedio<21.5 or promedio>27.0:
                    alerta=1
            elif (tipo==3):#gases 
                if promedio<0 or promedio>100:
                    alerta=1
            elif (tipo==1): #luz
                if promedio<100 or promedio>2000:
                    alerta=1
            else:   #ruido
                if promedio<0 or promedio>85:
                    alerta=1
       
        if(alerta==1):
            print("sensor fuera de rango")
            producer.send('alta.fueraderango',{'idSensor': str(id)})
            postAlerta(str(id), "Fuera de rango")

            
    ## caso en el que el valor recibido esta mal formado
    else:
        print("null value received")

        
