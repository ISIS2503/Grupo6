from rest_framework import serializers
from dashboard.models import Ubicacion, Tipo, MicroControlador,Alerta,Medicion,AlertaActuador

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

class MicroControladorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    ubicacion = serializers.UUIDField()
    estadoTemp = serializers.CharField()
    estadoGas = serializers.CharField()
    estadoSoni = serializers.CharField()
    estadoLuz = serializers.CharField()
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return MicroControlador.objects.create(**validated_data)


class MedicionSerializer(serializers.Serializer):
    idMedicion = serializers.IntegerField()
    idMicro = serializers.IntegerField()
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
    idSensor = serializers.IntegerField()
    promedio = serializers.IntegerField()
    def create(self, validated_data):
        """
        Create and return a new `PersonaModel` instance, given the validated data.
        """
        return Alerta.objects.create(**validated_data)
class AlertaActuadorSerializer(serializers.Serializer):
    idAlerta = serializers.IntegerField()
    tipoAlerta = serializers.CharField(required = False, max_length = 100)
    time = serializers.CharField()
    idActuador = serializers.IntegerField()
    def create(self,validated_data):
        return AlertaActuador.objects.create(**validated_data)
