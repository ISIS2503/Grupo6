import json

from kafka import KafkaConsumer

from chequeo import States

totalSensores=10000
numeroRangos=8

micros=[]

##valores variables
rango=1


# To consume latest messages and auto-commit offsets
consumer = KafkaConsumer('normal.'+'rango'+str(rango),group_id='my-group',bootstrap_servers=['172.24.42.23:8090'])


init=totalSensores/numeroRangos*(rango-1)
for i in range(int(totalSensores/numeroRangos)):
    micros.append(States.Sensor(init + i))
for message in consumer:
    jsonVal=json.loads(message.value)
    micros[jsonVal['id']].agregarTemperatura(jsonVal['temperatura'])
    micros[jsonVal['id']].agregarGas(jsonVal['gas'])
    micros[jsonVal['id']].agregarRuido(jsonVal['ruido'])
    micros[jsonVal['id']].agregarLuz(jsonVal['luz'])




