from django.db import models
from unittest.util import _MAX_LENGTH
from cassandra.cqlengine.connection import default
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel



#class Ubicacion(models.Model):
#    zona = models.IntegerField('zona', null = False)
#    area = models.IntegerField('area', null = False)
#    nivel = models.IntegerField('nivel', null = False)
class Ubicacion(DjangoCassandraModel):
    idUbicacion = columns.Integer(primary_key = True)
    zona = columns.Integer(required = False)
    area = columns.Integer(required = False)
    nivel = columns.Integer(required = False)

#class Alerta(models.Model):
#    id = models.BigIntegerField('id', primary_key = True)
#    tipoAlerta = models.CharField('tipoAlerta', max_length=128, null=True)
#    time= models.TimeField('time',default="06:00")
#    idUbicacion= models.ForeignKey(Ubicacion, null=True)
class Alerta(DjangoCassandraModel):
    idAlerta = columns.UUID(primary_key = True)
    tipoAlerta = columns.Text(required = False)
    time = columns.Time(required = True)
    idUbicacion = columns.UUID()

#class Tipo(models.Model):
#    nombre = models.CharField('nombre tipo',max_length = 23, null = False)
class Tipo(DjangoCassandraModel):
    idTipo = columns.UUID(primary_key = True)
    nombre = columns.Text(required = False)

#class Rango(models.Model):
#    valorMin = models.BigIntegerField('valorMin', null = False)
#    valorMax = models.BigIntegerField('valorMax', null = False)
class Rango(DjangoCassandraModel):
    valorMin = columns.Integer(required = False)
    valorMax = columns.Integer(required = False)
    idRango = columns.UUID(primary_key = True)

#class SensorUbicacion(models.Model):
#    idSensor = models.BigIntegerField(primary_key = True)
#    tipo = models.ForeignKey(Tipo, null = True)
#    ubicacion = models.ForeignKey(Ubicacion,null = True)

#class Sensor(models.Model):
#    idSensor = models.ForeignKey(SensorUbicacion)
#    time = models.TimeField('time')
#    valor= models.IntegerField('valor', null=False)
#    estado = models.CharField('estado', max_length = 1, null = True)
class Sensor(DjangoCassandraModel):
    idSensor = columns.UUID(primary_key = True)
    time = columns.Text(required = False)
    valor = columns.Integer(required = False)
    ubicacion = columns.UUID()

#class SubReporte (models.Model):
#    valMinimo=models.DecimalField(max_digits=7,decimal_places=3)
#    valMaximo=models.DecimalField(max_digits=7,decimal_places=3)
#    valPromedio = models.DecimalField(max_digits=7, decimal_places=3)
#    variacion = models.DecimalField(max_digits=7, decimal_places=3)
#    sensor=models.OneToOneField(Sensor)

#class Reporte(models.Model):
    #dia debe ser DateTimeField
#    dia= models.TimeField('dia')
#    anotaciones = models.CharField('anotaciones', max_length=1000)
    #faltan los suberportes

#class Usuarios(models.Model):
#    usuario = models.CharField('usuario', null=False, unique=True, max_length=64)
#    rol = models.CharField('rol', null=False, max_length=1)
#    contrasena= models.CharField('contraseña', null=False, max_length=128)
#    access_token = models.CharField('access_token', null=False, max_length=256)
#    reportes = models.ManyToManyField('reporte')
