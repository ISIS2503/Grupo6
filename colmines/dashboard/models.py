from django.db import models
from unittest.util import _MAX_LENGTH
from cassandra.cqlengine.connection import default
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
import time

class Ubicacion(DjangoCassandraModel):
    idUbicacion = columns.Integer(primary_key = True)
    zona = columns.Integer(required = False)
    area = columns.Integer(required = False)
    nivel = columns.Integer(required = False)


class Alerta(DjangoCassandraModel):
    idAlerta = columns.Integer(primary_key = True)
    tipoAlerta = columns.Text(required = False)
    time = columns.Text(required = True)
    idMicro = columns.Integer()
    promedio = columns.Integer()

class AlertaActuador(DjangoCassandraModel):
    idAlerta = columns.Integer(primary_key = True)
    tipoAlerta = columns.Text(required = False)
    time = columns.Text(required = True)
    idActuador = columns.Integer()

class Tipo(DjangoCassandraModel):
    idTipo = columns.UUID(primary_key = True)
    nombre = columns.Text(required = False)

class Rango(DjangoCassandraModel):
    valorMin = columns.Integer(required = False)
    valorMax = columns.Integer(required = False)
    idRango = columns.UUID(primary_key = True)

class MicroControlador(DjangoCassandraModel):
    id =columns.Integer(primary_key = True)
    ubicacion = columns.UUID()
    estadoTemp = columns.Text(required = True)
    estadoGas = columns.Text(required = True)
    estadoRuido = columns.Text(required = True)
    estadoLuz = columns.Text(required = True)
    def setEstado(self,key,val):
        if key == "estadoTemp":
            self.estadoTemp = val
        elif key == "estadoGas":
            self.estadoGas=val
        elif key == "estadoLuz":
            self.estadoLuz = val
        elif key == "estadoRuido":
            self.estadoRuido = val
        self.save()
class Medicion(DjangoCassandraModel):
    idMedicion =columns.Integer(primary_key = True)
    idMicro = columns.Integer(required= True)
    temperatura = columns.Integer(required= True)
    sonido = columns.Integer(required = True)
    gas = columns.Integer(required = True)
    luz = columns.Integer(required = True)
    time = columns.Text(required = True)
