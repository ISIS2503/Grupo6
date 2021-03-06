import time
import threading
import requests
import json
from kafka import KafkaProducer

# clase de objeto de los que heredan sensor y actuador

producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090','172.24.42.63:8090','172.24.42.24:8090'],
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))
ip = "172.24.42.46"

user = 'publisher'
passw = 'colmines12545'


class Sensor():
    def __init__(self, id):
        self.actuadorTemperatura = Actuador(id * 10)
        self.actuadorGas = Actuador(id * 10 + 1)
        self.actuadorLuz = Actuador(id * 10 + 2)
        self.actuadorRuido = Actuador(id * 10 + 3)
        self.cicloT = 0
        self.cicloG = 0
        self.cicloL = 0
        self.cicloR = 0
        self.id = id
        ya = time.time()
        self.tiempoTemperatura = ya
        self.tiempoGas = ya
        self.tiempoLuz = ya
        self.tiempoRuido = ya
        self.estadoTemperatura = Normal()
        self.estadoGas = Normal()
        self.estadoLuz = Normal()
        self.estadoRuido = Normal()
        self.temperaturas = []
        self.gases = []
        self.luces = []
        self.ruidos = []

    def calcularPomedio(self, lista, valor, tiempo):
        if (valor == None):
            return sum(lista) / len(lista)
        if (len(lista) != 10):
            lista.append(valor)
            promedio = sum(lista) / len(lista)
        else:
            lista.pop(0)
            lista.append(valor)
            promedio = sum(lista) / 10
        tiempo = time.time()
        return promedio

    def agregarTemperatura(self, valor):
        promedio = self.calcularPomedio(self.temperaturas, valor, self.tiempoTemperatura)
        tipo = "temperatura"
        self.goState(self.estadoTemperatura, promedio, 0, tipo)

    def agregarLuz(self, valor):
        tipo = "luz"
        self.goState(self.estadoLuz, self.calcularPomedio(self.luces, valor, self.tiempoLuz), 0, tipo)

    def agregarRuido(self, valor):
        tipo = "ruido"
        self.goState(self.estadoRuido, self.calcularPomedio(self.ruidos, valor, self.tiempoRuido), 0, tipo)

    def agregarGas(self, valor):
        tipo = "gas"
        self.goState(self.estadoGas, self.calcularPomedio(self.gases, valor, self.tiempoGas), 0, tipo)

    def cicloActuador(self, estado, ciclo, actuador):
        ciclo = ciclo + 1
        if ciclo == 1:
            actuador.cambiarEstado()
        if (estado.__class__ != FueraDeRango):
            actuador.cambiarEstado()
            ciclo = 0
        if ciclo == 6:
            ciclo = 0
            actuador.malFuncionamiento()
        # threading.Timer(600.0,self.cicloActuador,estado,ciclo,actuador).start()
        return ciclo

    def goState(self, estado, promedio, diferenciaTiempo, tipo):
        estado = estado.goState(promedio, diferenciaTiempo, tipo, self.id)
        if (estado.__class__ == FueraDeRango):
            if (tipo == "temperatura"):
                self.cicloT = self.cicloActuador(estado, self.cicloT, self.actuadorTemperatura)
            elif (tipo == "luz"):
                self.cicloL = self.cicloActuador(estado, self.cicloL, self.actuadorLuz)
            elif (tipo == "gas"):
                self.cicloG = self.cicloActuador(estado, self.cicloG, self.actuadorGas)
            elif (tipo == "ruido"):
                self.cicloR = self.cicloActuador(estado, self.cicloR, self.actuadorRuido)


class Actuador():
    def __init__(self, id):
        self.id = id
        self.incio = time.time()
        self.estado = Desactivado()
        self.ciclo = 0

    def cambiarEstado(self):
        self.goState(None)

    def malFuncionamiento(self):
        self.goState("F")

    def goState(self, fuera):
        self.estado = self.estado.goState(fuera, self.id)
        if (self.estado.__class__ == Activado):
            self.incio = time.time()


class EstadoSensor:
    pass


class EstadoActuador:
    pass


class Activado(EstadoActuador):
    def goState(self, des, id):
        if (des is None):
            publish(id, "desactivarActuador", "actuador", 0)
            return Desactivado()
        else:
            publish(id, "malFuncionamiento", "actuador", 0)
            postAlerta(id, "malFuncionamiento", "actuador", 0)
            return MalFuncionamiento()


class Desactivado(EstadoActuador):
    def goState(self, des, id):
        if (des is None):
            postAlerta(id, "activado", "actuador", 0)
            return Activado()

        else:
            publish(id, "malFuncionamiento", "actuador", 0)
            postAlerta(id, "malFuncionamiento", "actuador", 0)
            return MalFuncionamiento()


class MalFuncionamiento(EstadoActuador):
    def goState(self, des, id):
        if (des == None):
            return Desactivado()
        else:
            publish(id, "malFuncionamiento", "actuador", 0)
            postAlerta(id, "malFuncionamiento", "actuador", 0)
            return MalFuncionamiento()


class FueraDeLinea(EstadoSensor):
    def goState(self, promedio, diferenciaTiempo, tipo, id):
        if (diferenciaTiempo >= 300):
            return FueraDeLinea()
        putEstado(id, Normal(), tipo)
        return Normal()


class Normal(EstadoSensor):
    def goState(self, promedio, diferenciaTiempo, tipo, id):
        if (diferenciaTiempo >= 300):
            publish(id, "fueraDeLinea", tipo, promedio)
            postAlerta(id, "fueraDeLinea", tipo, promedio)
            putEstado(id, FueraDeLinea(), tipo)
            return FueraDeLinea()
        if (tipo == "temperatura"):
            if promedio < 21.5 or promedio > 27.0:
                publish(id, "fueraDeRango", tipo, promedio)
                postAlerta(id, "fueraDeRango", tipo, promedio)
                putEstado(id, FueraDeRango(), tipo)
                return FueraDeRango()
        elif (tipo == "luz"):
            if promedio < 100 or promedio > 2000:
                publish(id, "fueraDeRango", tipo, promedio)
                postAlerta(id, "fueraDeRango", tipo, promedio)
                putEstado(id, FueraDeRango(), tipo)
                return FueraDeRango()
        elif (tipo == "gas"):
            if promedio < 0 or promedio > 100:
                publish(id, "fueraDeRango", tipo, promedio)
                postAlerta(id, "fueraDeRango", tipo, promedio)
                putEstado(id, FueraDeRango(), tipo)
                return FueraDeRango()
        elif (tipo == "ruido"):
            if promedio < 0 or promedio > 85:
                publish(id, "fueraDeRango", tipo, promedio)
                postAlerta(id, "fueraDeRango", tipo, promedio)
                putEstado(id, FueraDeRango(), tipo)
                return FueraDeRango()
        return self


class FueraDeRango(EstadoSensor):
    def goState(self, promedio, diferenciaTiempo, tipo, id):
        if (diferenciaTiempo >= 300):
            publish(id, "fueraDeLinea", tipo, promedio)
            postAlerta(id, "fueraDeLinea", tipo, promedio)
            putEstado(id, FueraDeLinea(), tipo)
            return FueraDeLinea()
        if (tipo == "temperatura"):
            if promedio < 21.5 or promedio > 27.0:
                return FueraDeRango()
        elif (tipo == "luz"):
            if promedio < 100 or promedio > 2000:
                return FueraDeRango()
        elif (tipo == "gas"):
            if promedio < 0 or promedio > 100:
                return FueraDeRango()
        elif (tipo == "ruido"):
            if promedio < 0 or promedio > 85:
                return FueraDeRango()
        putEstado(id, Normal(), tipo)
        return Normal()


def publish(id, tipoAlerta, tipoEntidad, promedio):
    # global producer
    producer = KafkaProducer(bootstrap_servers=['172.24.42.23:8090','172.24.42.63:8090','172.24.42.24:8090'],
                             value_serializer=lambda m: json.dumps(m).encode('ascii'))
    print("publicacion " + tipoAlerta)
    payload = {
        "idMicro": id,
        "tipoEntidad": tipoEntidad,
        "promedio": promedio
    }
    res = producer.send('alta.' + tipoAlerta, payload)
    print("enviando alerta: " + 'alta.', tipoAlerta + " " + tipoEntidad + "...")
    #print(res)


def postAlerta(id, tipoAlerta, tipoEntidad, promedio):
    try:
        if (tipoEntidad == "actuador"):
            payload = {

                "tipoAlerta": tipoAlerta,
                "time": str(time.time()),
                "idActuador": id,
                "tipoEntidad": tipoEntidad
            }
            url = "http://" + ip + ":8080/rest/alertas/actuador"
        else:
            payload = {

                "idMicro": id,
                "time": str(time.time()),
                "tipoAlerta": tipoAlerta,
                "promedio": int(promedio), ##por ahora
                "tipoEntidad": tipoEntidad
            }
            url = "http://" + ip + ":8080/rest/alertas/sensores"

        response = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
        print(str(id) + " Tipo Alerta: " + tipoAlerta + " Response Status code: " + str(response.status_code))
        #print(json.dumps(payload))
    except requests.exceptions.ConnectionError:
        print("Exception at posting")


def putEstado(id, estado, tipo):
    print("cambio de estado para el sensor " + str(id))
    if estado.__class__ == FueraDeRango:
        est = "FueraDeRango"
    elif estado.__class__ == Normal:
        est = "Normal"
    elif estado.__class__ == FueraDeLinea:
        est = "FueraDeLinea"
    payload = {
        "estadoJ": 0
    }
    if (tipo == "temperatura"):
        payload = {

            "estadoTemp": est

        }
    elif (tipo == "luz"):
        payload = {

            "estadoLuz": est
        }
    elif (tipo == "gas"):
        payload = {

            "estadoGas": est
        }
    elif (tipo == "ruido"):
        payload = {

            "estadoRuido": est
        }

    url = "http://" + ip + ":8080/rest/micro/" + str(id)

    response = requests.put(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    print("PUT Response Status code: " + str(response.status_code))
    #print(url)
    #print(json.dumps(payload))
