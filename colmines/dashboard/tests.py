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
        self.ubicacion = Ubicacion.objects.create(id=10, zona= 10, area= 10, nivel=10)

    # test that detail page returns a 200 if the item exists
    def testCreateUbicacion(self):
        ub=Ubicacion.objects.get(id=10)
        self.assertEqual(ub.id, 10)
        self.assertEqual(ub.zona, 10)
        self.assertEqual(ub.area, 10)
        self.assertEqual(ub.nivel, 10)

class TestTipo(TestCase):
    
    def setUp(self):
        self.tipo = Tipo.objects.create(id=10, nombre="Temperatura")
    
    # test that detail page returns a 200 if the item exists
    def testCreateTipo(self):
        tipo=Tipo.objects.get(id=10)
        self.assertEqual(tipo.id, 10)
        self.assertEqual(tipo.nombre, "Temperatura")


class TestAlerta(TestCase):
    
    def setUp(self):
        self.ubicacion = Ubicacion.objects.create(id=10, zona= 10, area= 10, nivel=10)
        self.time=datetime.datetime.now()
        self.alerta = Alerta.objects.create(id=10, tipoAlerta="Temperatura fuera de rango", time=self.time, idUbicacion=self.ubicacion)


    # test that detail page returns a 200 if the item exists
    def testCreateAlerta(self):
        al=Alerta.objects.get(id=10)
        self.assertEqual(al.id, 10)
        self.assertEquals(al.tipoAlerta,"Temperatura fuera de rango")
       # self.assertEqual(al.time, self.time)
        self.assertEqual(al.idUbicacion, self.ubicacion)


class TestRango(TestCase):
    
    def setUp(self):

        self.rango = Rango.objects.create(id=10,valorMin=10, valorMax=20);

            
        # test that detail page returns a 200 if the item exists
    def testCreateRango(self):
        ra=Rango.objects.get(id=10)
        self.assertEqual(ra.id, 10)
        self.assertEqual(ra.valorMin, 10)
        self.assertEqual(ra.valorMax, 20)


class TestSensor(TestCase):
    
    def setUp(self):
        self.ubicacion = Ubicacion.objects.create(id=10, zona= 10, area= 10, nivel=10)
        self.tipo = Tipo.objects.create(id=10, nombre="Temperatura")
        self.time=datetime.datetime.now()
        self.sensUb= SensorUbicacion.objects.create( idSensor=0, tipo=self.tipo, ubicacion=self.ubicacion)

        self.sensor = Sensor.objects.create(id=10,idSensor=self.sensUb, time= self.time, valor=10,estado='N')


    # test that detail page returns a 200 if the item exists
    def testCreate(self):
        sens=Sensor.objects.get(id=10)
        self.assertEqual(sens.idSensor, self.sensUb)
        #self.assertEqual(sens.time, self.time)
        self.assertEqual(sens.valor, 10)
        self.assertEqual(sens.estado, 'N')


class TestSensorUb(TestCase):

    def setUp(self):
        self.tipo = Tipo.objects.create(id=10, nombre="Temperatura")

        self.ubicacion = Ubicacion.objects.create(id=10, zona= 10, area= 10, nivel=10)
        self.sensUb= SensorUbicacion.objects.create(idSensor=0, tipo=self.tipo)



    # test that detail page returns a 200 if the item exists
    def testCreate(self):
        sens=SensorUbicacion.objects.get(idSensor=0)
        self.assertEqual(sens.idSensor, 0)
        self.assertEqual(sens.tipo,self.tipo)
        
       


##hasta aqui esta bien
##******************************************************************************************************

class TestSubReporte(TestCase):
    
    def setUp(self):
        self.ubicacion = Ubicacion.objects.create(id=10, zona= 10, area= 10, nivel=10)
        self.tipo = Tipo.objects.create(id=10, nombre="Temperatura")
        self.time=datetime.datetime.now()
        self.sensUb= SensorUbicacion.objects.create(idSensor=0, tipo=self.tipo, ubicacion=self.ubicacion)
        self.sensor = Sensor.objects.create(id=10,idSensor=self.sensUb, time= self.time, valor=10,estado='N')
        self.subreporte = SubReporte.objects.create(id=0,valMinimo=10,valMaximo=50,valPromedio=10,variacion=0.2,sensor=self.sensor)
        self.reporte = Reporte("ANOTA")
        self.usuario = Usuarios("Juan","ADMIN","1234","AT11",self.reporte)

    # test that detail page returns a 200 if the item exists
    def testCreateSubReporte(self):
        sub=SubReporte.objects.get(id=0)
        self.assertEqual(sub.id, 0)
        self.assertEqual(sub.valMinimo, 10)
        self.assertEqual(sub.valMaximo, 50)

class TestReporte(TestCase): 
    
    def setUp(self):
        Reporte.objects.create(id=10,dia=datetime.datetime.now(),anotaciones="jesus nos ilumino")
    # test that detail page returns a 200 if the item exists
    def testCreateReporte(self):
        rep=Reporte.objects.get(id=10)
        self.assertEqual(rep.id, 10)
        
        self.assertEqual(rep.anotaciones, "jesus nos ilumino")
    
class TestUsuarios(TestCase):
    
    def setUp(self):
        self.reporte=Reporte.objects.create(id=10,dia=datetime.datetime.now(),anotaciones="jesus nos ilumino")

        self.usuario = Usuarios.objects.create(id=10,usuario="Juan",rol="A",contrasena="1234",access_token="AT11")
    # test that detail page returns a 200 if the item exists
    def testCreateUsuario(self):
        us=Usuarios.objects.get(id=10)
        self.assertEqual(us.id, 10)
        self.assertEqual(us.usuario, "Juan")
        self.assertEqual(us.rol, "A")
        self.assertEqual(us.contrasena, "1234")
