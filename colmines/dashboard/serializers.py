from rest_framework import serializers
from dashboard.models import Ubicacion, Tipo, Sensor, SensorUbicacion

class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields =('id','zona','area','nivel')
class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields =('id','nombre')

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields =  ('idSensor','time', 'valor', 'estado')

class SensorUbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorUbicacion
        fields = ('idSensor','tipo','ubicacion')