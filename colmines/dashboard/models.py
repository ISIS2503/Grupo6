from django.db import models
from unittest.util import _MAX_LENGTH
from cassandra.cqlengine.connection import default
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel
import time

class Ubicacion(DjangoCassandraModel):
    idUbicacion = columns.Integer(primary_key = True)
    zona = columns.Integer(required = True)
    area = columns.Integer(required = True)
    nivel = columns.Integer(required = True)


class Alerta(DjangoCassandraModel):
    idAlerta = columns.Integer(primary_key = True)
    tipoAlerta = columns.Text(required = True)
    time = columns.Text(required = True)
    idMicro = columns.Integer(required = True)
    promedio = columns.Double(required = True)
    tipoEntidad = columns.Text(required = True)

class AlertaActuador(DjangoCassandraModel):
    idAlerta = columns.Integer(primary_key = True)
    tipoAlerta = columns.Text(required = False)
    time = columns.Text(required = True)
    idActuador = columns.Integer()
    tipoEntidad = columns.Text(required = True)


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
