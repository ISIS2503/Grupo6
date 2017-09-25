from django.db import models

class Sensor(models.Model):
    id = models.BigIntegerField('id', primary_key = True)
    valor= models.IntegerField('valor', null=False)
    estado = models.CharField('estado', null = False)
    time = models.TimeField('time', null = False)
    tipo = models.OneToOneField(Tipo, related_name = 'tipo', blank=False)
    ubicacion = models.ManyToOneRel(Ubicacion, related_name ='ubicacion', blank = False)
    