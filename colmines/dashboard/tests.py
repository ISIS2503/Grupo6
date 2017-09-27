#
# from django.conf import settings
#
# settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
#     TEMPLATE_DIRS=('/home/web-apps/dashboard', '/home/web-apps/base'))
# import django
# django.setup()
import datetime
from django.test import TestCase
#from django.core.urlresolvers import reverse

from .models import *

class TestUbicacion(TestCase):

    # ran before each test.
    def setUp(self):
        self.ubicacion = Ubicacion.objects.create(zona= 10, area= 10, nivel=10)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        ub=Ubicacion.objects.get(id=10)
        self.assertEqual(ub.id, 10)
        self.assertEqual(ub.zona, 10)
        self.assertEqual(ub.area, 10)
        self.assertEqual(ub.nivel, 10)

class TestTipo(TestCase):
    
    def setUp(self):
        self.tipo = Tipo(10,"Temperatura")
    
    # test that detail page returns a 200 if the item exists
    def testCreateTipo(self):
        self.assertEqual(self.tipo.id, 10)
        self.assertEqual(self.tipo.nombre, "Temperatura")

#Falta arreglar de aquí para abajo
class TestAlerta(TestCase):
    
    def setUp(self):

        self.alerta = Alerta(10)


    # test that detail page returns a 200 if the item exists
    def testCreateAlerta(self):
        self.assertEqual(self.alerta.id, 10)


class TestRango(TestCase):
    
    def setUp(self):

        self.rango = Rango(10,10,20);


    # test that detail page returns a 200 if the item exists
    def testCreateRango(self):
        self.assertEqual(self.rango.id, 10)
        self.assertEqual(self.rango.valorMin, 10)
        self.assertEqual(self.rango.valorMax, 20)


class TestSensor(TestCase):
    
    def setUp(self):

        self.time=datetime.datetime.now()
        self.sensor = Sensor(10, self.time, 10,'N')


    # test that detail page returns a 200 if the item exists
    def testCreate(self):
        self.assertEqual(self.ubicacion.idSensor, 10)
        self.assertEqual(self.ubicacion.time, self.time)
        self.assertEqual(self.ubicacion.valor, 10)
        self.assertEqual(self.ubicacion.estado, 'N')

class TestSensorUb(TestCase):

    def setUp(self):

        self.time=datetime.datetime.now()
        self.sensor = Sensor(10, self.time, 10,'N')


    # test that detail page returns a 200 if the item exists
    def testCreate(self):
        self.assertEqual(self.ubicacion.idSensor, 10)
        self.assertEqual(self.ubicacion.time, self.time)
        self.assertEqual(self.ubicacion.valor, 10)
        self.assertEqual(self.ubicacion.estado, 'N')


class TestSubReporte(TestCase):
    
    def setUp(self):
        self.ubicacion = Ubicacion(10,10,10,10)
        self.tipo = Tipo(10,"Temperatura")
        self.alerta = Alerta(10)
        self.rango = Rango(10,10,20);
        self.sensor = Sensor(10,10,"ACTIVO")
        self.subreporte = SubReporte(0,10,5,10,self.sensor)
        self.reporte = Reporte("ANOTA")
        self.usuario = Usuarios("Juan","ADMIN","1234","AT11",self.reporte)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        self.assertEqual(self.ubicacion.id, 10)
        self.assertEqual(self.ubicacion.zona, 10)
        self.assertEqual(self.ubicacion.area, 10)
        self.assertEqual(self.ubicacion.nivel, 10)

class TestReporte(TestCase): 
    
    def setUp(self):
        self.ubicacion = Ubicacion(10,10,10,10)
        self.tipo = Tipo(10,"Temperatura")
        self.alerta = Alerta(10)
        self.rango = Rango(10,10,20);
        self.sensor = Sensor(10,10,"ACTIVO")
        self.subreporte = SubReporte(0,10,5,10,self.sensor)
        self.reporte = Reporte("ANOTA")
        self.usuario = Usuarios("Juan","ADMIN","1234","AT11",self.reporte)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        self.assertEqual(self.ubicacion.id, 10)
        self.assertEqual(self.ubicacion.zona, 10)
        self.assertEqual(self.ubicacion.area, 10)
        self.assertEqual(self.ubicacion.nivel, 10)
    
class TestUsuarios(TestCase):
    
    def setUp(self):
        self.ubicacion = Ubicacion(10,10,10,10)
        self.tipo = Tipo(10,"Temperatura")
        self.alerta = Alerta(10)
        self.rango = Rango(10,10,20);
        self.sensor = Sensor(10,10,"ACTIVO")
        self.subreporte = SubReporte(0,10,5,10,self.sensor)
        self.reporte = Reporte("ANOTA")
        self.usuario = Usuarios("Juan","ADMIN","1234","AT11",self.reporte)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        self.assertEqual(self.ubicacion.id, 10)
        self.assertEqual(self.ubicacion.zona, 10)
        self.assertEqual(self.ubicacion.area, 10)
        self.assertEqual(self.ubicacion.nivel, 10)
