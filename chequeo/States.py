import time
import threading
import requests
import json
from kafka import KafkaProducer
#clase de objeto de los que heredan sensor y actuador

producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090'], value_serializer=lambda m: json.dumps(m).encode('ascii'))

class Sensor():
    def __init__(self,id):
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

    def goState(self, estado, promedio,diferenciaTiempo,tipo):
        estado=estado.goState(promedio,diferenciaTiempo,tipo)


class Actuador():
    def __init__(self,id):
        self.id=id
        self.incio=time.time()
        self.estado=Activado()
    def desactivar(self):
        self.goState(None)
    def activar(self):
        self.goState(None)
    def chequearConexion(self):
        ya=time.time()
        if (ya-self.incio>=3600 and self.estado.__class__==Activado):
            self.goState("F")
        threading.Timer(3000.0,self.chequearConexion).start()

    def goState(self,fuera):
        self.estado=self.estado.goState(fuera)
        if (self.estado.__class__==Activado):
            self.incio=time.time()

class EstadoSensor:
    pass

class EstadoActuador:
    pass

class Activado(EstadoActuador):
    def goState(self,des,id):
        if(des==None):
            return Desactivado()
        else:
            i=IndependentProducer(id,"malFuncionamiento",True,"actuador")
            i.start()
            return MalFuncionamiento()

class Desactivado(EstadoActuador):
    def goState(self, des,id):
        if(des==None):
            return Activado()
        else:
            i=IndependentProducer(id,"malFuncionamiento",True,"actuador")
            i.start()
            return MalFuncionamiento()

class MalFuncionamiento(EstadoActuador):
    def goState(self,des,id):
        if(des==None):
            return Desactivado()
        else:
            i=IndependentProducer(id,"malFuncionamiento",True,"actuador")
            i.start()
            return MalFuncionamiento()

class FueraDeLinea(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            return FueraDeLinea()
        return Normal()

class Normal(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            i=IndependentProducer(id,"fueraDeLinea",True,tipo)
            i.start()
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif (tipo=="gaz"):
            if promedio<0 or promedio>100:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()

class FueraDeRango(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo,id):
        if (diferenciaTiempo>=300):
            i=IndependentProducer(id,"fueraDeLinea",True,tipo)
            i.start()
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif (tipo=="gaz"):
            if promedio<0 or promedio>100:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                i=IndependentProducer(id,"fueraDeRango",True,tipo)
                i.start()
                return FueraDeRango()
        return Normal()


#la siguiente clase será encarcgada de hacer la publicación en Kafka y el post
#la idea es no dejar bloqueado el script mientras se hacen estas acciones
class IndependentProducer(threading.Thread):
    def __init__(self,id, tipoAlerta,alerta, tipoEntidad):
        threading.Thread.__init__(self)
        self.tipoEntidad=tipoEntidad
        self.tipoAlerta=tipoAlerta
        self.id=id
        self.alerta=alerta
    def run(self):
        try:
            if self.alerta:
                print("alerta "+self.tipoAlerta)
                producer.send('alta.'+self.tipoAlerta,{'idSensor': str(self.id), 'tipo': str(self.tipoEntidad)})
                print("enviando alerta: "+ self.tipoAlerta + " " +self.tipoEntidad+"...")
                url="http://localhost:8000/alertas/"
                payload = {
                    "idSensor" : self.id,
                    "tipoEntidad": self.tipoEntidad,
                    "timeStamp" : str(time.time()),
                    "tipoAlerta" : self.tipoAlerta
                }
            response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
            print(str(self.id) + " Tipo Alerta: "+self.tipoAlerta+ " Response Status code: " + str(response.status.code))
        except ValueError:
            print(ValueError)
