import time
import threading
#clase de objeto de los que heredan sensor y actuador
class EntidadFisica:
    def __init__(self, id):
        self.id=id

class Sensor(EntidadFisica):
    def __init__(self):
        EntidadFisica.__init__(self)
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


class Actuador(EntidadFisica):
    def __init__(self):
        self.incio=time.time()
        self.estado=Activado()
    def desactivar(self):
        self.goState(None)
    def activar(self):
        self.goState(None)
    def chequearConexion(self):
        ya=time.time()
        if (ya-self.incio):
            self.goState("F")
        threading.Timer(3000.0,self.chequearConexion).start()
    def goState(self,fuera):
        self.estado=self.estado.goState(fuera)

class EstadoSensor:
    def goState(self):

class EstadoActuador:
    def goState(self):

class Activado(EstadoActuador):
    def goState(self,des):
        if(des==None):
            return Desactivado()
        else:
            return MalFuncionamiento()

class Desactivado(EstadoActuador):
    def goState(self, des):
        if(des==None):
            return Activado()
        else:
            return MalFuncionamiento()

class MalFuncionamiento(EstadoActuador):
    def goState(self,des):
        if(des==None):
            return Desactivado()
        else:
            return MalFuncionamiento()

class FueraDeLinea(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo):
        if (diferenciaTiempo>=300):
            return FueraDeLinea()
        return Normal()

class Normal(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo):
        if (diferenciaTiempo>=300):
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                return FueraDeRango()
        elif (tipo=="gaz"):
            if promedio<0 or promedio>100:
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                return FueraDeRango()
        return Normal

class FueraDeRango(EstadoSensor):
    def goState(self,promedio,diferenciaTiempo,tipo):
        if (diferenciaTiempo>=300):
            return FueraDeLinea()
        if (tipo=="temperatura"):
            if promedio<21.5 or promedio>27.0:
                return FueraDeRango()
        elif (tipo=="luz"):
            if promedio<100 or promedio>2000:
                return FueraDeRango()
        elif (tipo=="gaz"):
            if promedio<0 or promedio>100:
                return FueraDeRango()
        elif(tipo=="ruido"):
            if promedio<0 or promedio>85:
                return FueraDeRango()
        return Normal()

