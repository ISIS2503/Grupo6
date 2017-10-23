import time
import threading
import requests
import json
from kafka import KafkaProducer
#clase de objeto de los que heredan sensor y actuador

producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090'], value_serializer=lambda m: json.dumps(m).encode('ascii'))
ip="172.24.42.40"

class Sensor():
    def __init__(self,id):
        self.actuador=Actuador()
        self.ciclo=0
        self.id=id
        ya=time.time()
        self.tiempoTemperatura=ya
        self.tiempoGas=ya
        self.tiempoLuz=ya
        self.tiempoRuido=ya
        self.estadoTemperatura=Normal()
        self.estadoGas=Normal()
        self.estadoLuz=Normal()
        self.estadoRuido=Normal()
        self.temperaturas=[]
        self.gases=[]
        self.luces=[]
        self.ruidos=[]
        self.chequearConexion()

    def chequearConexion(self):
        ya=time.time()
        if(ya-self.tiempoGas>=300):
            self.goState(self.estadoGas,0,350,"")
        if(ya-self.tiempoRuido>=300):
            self.goState(self.estadoRuido,0,350,"")
        if(ya-self.tiempoLuz>=300):
            self.goState(self.estadoLuz,0,350,"")
        if(ya-self.tiempoTemperatura>=300):
            self.goState(self.estadoTemperatura,0,350,"")
        threading.Timer(300.0,self.chequearConexion).start()

    def calcularPomedio(self, lista, valor, tiempo):
        if(valor==None):
            return sum(lista)/len(lista)
        if (len(lista)!=10):
            lista.append(valor)
            promedio=sum(lista)/len(lista)
        else:
            lista.pop(0)
            lista.append(valor)
            promedio=sum(lista)/10
        tiempo=time.time()
        return promedio

    def agregarTemperatura(self,valor):
        promedio=self.calcularPromedio(self.temperaturas,valor,self.tiempoTemperatura)
        self.goState(self.estadoTemperatura,promedio,0,"temperatura")
    def agregarLuz(self,valor):
        self.goState(self.estadoLuz, self.calcularPromedio(self.luces,valor,self.tiempoLuz,0,"luz"))
    def agregarRuido(self,valor):
        self.goState(self.estadoRuido, self.calcularPromedio(self.ruidos,valor,self.tiempoRuido,0,"ruido"))
    def agregarGas(self,valor):
        self.goState(self.estadoGas, self.calcularPromedio(self.gases,valor,self.tiempoGas,0),0,"gas")

    def cicloActuador(self,estado):
        self.ciclo=self.ciclo+1
        if(estado.__class__!=FueraDeRango):
            self.actuador.cambiarEstado()
            self.ciclo=0
        if self.ciclo==6:
            self.ciclo=0
            self.actuador.malFuncionamiento()
        threading.Timer(600.0,self.cicloActuador,estado).start()

    def goState(self, estado, promedio,diferenciaTiempo,tipo):
        estado=estado.goState(promedio,diferenciaTiempo,tipo)
        if(estado.__class__==FueraDeRango):
            self.actuador.cambiarEstado()
            self.cicloActuador(estado)



class Actuador():
    def __init__(self,id):
        self.id=id
        self.incio=time.time()
        self.estado=Desactivado()
        self.ciclo=0
    def cambiarEstado(self):
        self.goState(None)
    def malFuncionamiento(self):
        self.goState("F")
    def goState(self,fuera):
        self.estado=self.estado.goState(fuera)
        if (self.estado.__class__==Activado):
            self.incio=time.time()
            self.cicloActuador()

class EstadoSensor:
    pass

class EstadoActuador:
    pass

class Activado(EstadoActuador):
    def goState(self,des,id):
        if(des==None):
            publish(id,"desactivarActuador","actuador")
            return Desactivado()
        else:
            publish(id,"malFuncionamiento","actuador")
            postAlerta(id,"malFuncionamiento","actuador")
            return MalFuncionamiento()

class Desactivado(EstadoActuador):
    def goState(self, des,id):
        if(des==None):
            return Activado()
        else:
            publish(id,"malFuncionamiento","actuador")
            postAlerta(id,"malFuncionamiento","actuador")
            return MalFuncionamiento()

class MalFuncionamiento(EstadoActuador):
    def goState(self,des,id):
        if(des==None):
            return Desactivado()
        else:
            publish(id,"malFuncionamiento","actuador")
            postAlerta(id,"malFuncionamiento","actuador")
            return MalFuncionamiento()

class FueraDeLinea(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            return FueraDeLinea()
        putEstado(id,Normal(),tipo)
        return Normal()

class Normal(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            publish(id,"fueraDeLinea",tipo, promedio)
            postAlerta(id,"fueraDeLinea",tipo, promedio)
            putEstado(id,FueraDeLinea(),tipo)
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif (tipo=="gas"):
            if promedio<0 or promedio>100:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        return self

class FueraDeRango(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            publish(id,"fueraDeLinea",tipo, promedio)
            postAlerta(id,"fueraDeLinea",tipo, promedio)
            putEstado(id,FueraDeLinea(),tipo)
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif (tipo=="gas"):
            if promedio<0 or promedio>100:
                publish(id,"fueraDeRango",tipo, promedio)
                postAlerta(id,"fueraDeRango",tipo, promedio, promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                publish(id,"fueraDeRango",tipo,promedio)
                postAlerta(id,"fueraDeRango",tipo,promedio)
                putEstado(id,FueraDeRango(),tipo)
                return FueraDeRango()
        putEstado(id,Normal(),tipo)
        return Normal()




def publish(id, tipoAlerta, tipoEntidad, promedio):
    print("publicacion "+tipoAlerta)
    payload = {
        "idSensor" : id,
        "tipoEntidad": tipoEntidad,
        "promedio"  : promedio
    }
    producer.send('alta.'+tipoAlerta,payload)
    print("enviando alerta: "+ tipoAlerta + " " +tipoEntidad+"...")

def postAlerta(id, tipoAlerta, tipoEntidad, promedio):
    if (tipoEntidad=="actuador"):
        payload={
         "idActuador":id,
         "time" : str(time.time()),
         "tipoAlerta" : tipoAlerta
        }
        url="http://"+ip+":8080/alertas/actuador"
    else:
        payload = {
            "idSensor" :id,
            "time" : str(time.time()),
            "tipoAlerta" : tipoAlerta,
            "promedio" : promedio
        }
        url="http://"+ip+":8080/alertas/sensores"

    response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    print(str(id) + " Tipo Alerta: "+tipoAlerta+ " Response Status code: " + str(response.status.code))

def putEstado(id,estado,tipo):
    print("cambio de estado para el sensor "+id)
    if estado.__class__==FueraDeRango:
        est="FueraDeRango"
    elif estado.__class__==Normal:
        est="Normal"
    elif estado.__class__==FueraDeLinea:
        est="FueraDeLinea"
    if (tipo=="temperatura"):
            payload={
         "id":id,
         "estadoTemp" : est
         
        }
    elif (tipo=="luz"):
         payload={
     "id":id,
     "estadoLuz": est
    }
    elif (tipo=="gas"):
         payload={
     "id":id,
     "estadoGas": est
    }
    elif(tipo=="ruido"):
         payload={
     "id":id,
     "estadoRuido" : est
    }
    url="http://"+ip+":8080/micro/"+id

    response = requests.put(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    print(" Response Status code: " + str(response.status.code))
