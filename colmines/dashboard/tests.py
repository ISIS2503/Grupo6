from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import *


class TestUbicacion(TestCase):

    # ran before each test.
    def setUp(self):
        self.ubicacion = Ubicacion(10,10,10,10)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        self.assertEqual(self.ubicacion.id, 10)
        self.assertEqual(self.ubicacion.zona, 10)
        self.assertEqual(self.ubicacion.area, 10)
        self.assertEqual(self.ubicacion.nivel, 10)

class TestTipo(TestCase):
    
    def setUp(self):
        self.tipo = Tipo(10,"Temperatura")
    
    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        self.assertEqual(self.ubicacion.id, 10)
        self.assertEqual(self.ubicacion.nombre, "Temperatura")

#Falta arreglar de aquí para abajo
class TestAlerta(TestCase):
    
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

class TestRango(TestCase):
    
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

class TestSensor(TestCase):
    
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
