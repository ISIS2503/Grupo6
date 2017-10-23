from rest_framework import serializers
from dashboard.models import Ubicacion, Tipo, Sensor,Alerta,Medicion

class UbicacionSerializer(serializers.Serializer):
    idUbicacion = serializers.IntegerField()
    zona = serializers.IntegerField(required = False)
    area = serializers.IntegerField(required = False)
    nivel = serializers.IntegerField(required = False)
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return Ubicacion.objects.create(**validated_data)

class TipoSerializer(serializers.Serializer):
    idTipo = serializers.UUIDField()
    nombre = serializers.CharField(required = False, max_length = 100)
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return Tipo.objects.create(**validated_data)

class SensorSerializer(serializers.Serializer):
    idSensor = serializers.IntegerField()
    ubicacion = serializers.UUIDField()
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return Sensor.objects.create(**validated_data)
class MedicionSerializer(serializers.Serializer):
    idMedicion = serializers.IntegerField()
    idSensor0 = serializers.IntegerField()
    idSensor1 = serializers.IntegerField()
    idSensor2 = serializers.IntegerField()
    idSensor3 = serializers.IntegerField()
    temperatura = serializers.IntegerField()
    sonido = serializers.IntegerField()
    gas = serializers.IntegerField()
    luz = serializers.IntegerField()
    time = serializers.CharField()
    def create(self,validated_data):
        return Medicion.objects.create(**validated_data)

class AlertaSerializer(serializers.Serializer):
    idAlerta = serializers.IntegerField()
    tipoAlerta = serializers.CharField(required = False, max_length=100)
    time = serializers.CharField()
    idUbicacion = serializers.IntegerField()
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return Alerta.objects.create(**validated_data)
