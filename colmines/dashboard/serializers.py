from rest_framework import serializers
from dashboard.models import Ubicacion, Tipo, Sensor

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
        fields =  ('id','time', 'valor', 'estado', 'tipo', 'ubicacion')
