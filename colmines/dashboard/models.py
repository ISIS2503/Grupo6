from django.db import models
from unittest.util import _MAX_LENGTH
from cassandra.cqlengine.connection import default

class Ubicacion(models.Model):
    zona = models.IntegerField('zona', null = False)
    area = models.IntegerField('area', null = False)
    nivel = models.IntegerField('nivel', null = False)
    
class Tipo(models.Model):
    nombre = models.CharField('nombre tipo',max_length = 23, null = False)
   
class Alerta(models.Model):
    id = models.BigIntegerField('id', primary_key = True)
    
    
class Rango(models.Model):
      
    valorMin = models.BigIntegerField('valorMin', null = False)
    valorMax = models.BigIntegerField('valorMax', null = False)


class SensorUbicacion(models.Model):
    idSensor = models.BigIntegerField(primary_key = True)
    tipo = models.ForeignKey(Tipo, null = True)
    ubicacion = models.ForeignKey(Ubicacion,null = True)   

class Sensor(models.Model):
    idSensor = models.ForeignKey(SensorUbicacion)
    time = models.TimeField('time')
    valor= models.IntegerField('valor', null=False)
    estado = models.CharField('estado', max_length = 1, null = False) 


class SubReporte (models.Model):
    valMinimo=models.DecimalField(max_digits=7,decimal_places=3)
    valMaximo=models.DecimalField(max_digits=7,decimal_places=3)
    valPromedio = models.DecimalField(max_digits=7, decimal_places=3)
    variacion = models.DecimalField(max_digits=7, decimal_places=3)
    sensor=models.OneToOneField(Sensor)
    
class Reporte(models.Model):
    dia= models.TimeField('dia')
    anotaciones = models.CharField('anotaciones', max_length=1000)
    
class Usuarios(models.Model):
    usuario = models.CharField('usuario', null=False, unique=True, max_length=64)
    rol = models.CharField('rol', null=False, max_length=1)
    contrasena= models.CharField('contraseña', null=False, max_length=128)
    access_token = models.CharField('access_token', null=False, max_length=256)
    reportes = models.ManyToManyField('reporte')
