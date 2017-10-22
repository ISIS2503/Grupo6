from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dashboard.models import Ubicacion,Tipo,Sensor
from dashboard.serializers import UbicacionSerializer,TipoSerializer,SensorSerializer
from django.template.context_processors import request

def index(request):
    context = {

    }
    return render(request, 'dashboard/index.html', context)
@csrf_exempt

def ubicacion_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Ubicacion.objects.all()
        serializer = UbicacionSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UbicacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tipo_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Tipo.objects.all()
        serializer = TipoSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TipoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def sensor_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Sensor.objects.all()
        serializer = SensorSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SensorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
#def sensor_ubicacion_list(request):
    """
    List all code snippets, or create a new snippet.
    """
#    if request.method == 'GET':
#        snippets = SensorUbicacion.objects.all()
#        serializer = SensorUbicacionSerializer(snippets, many=True)
#        return JsonResponse(serializer.data, safe=False)
#
#    elif request.method == 'POST':
#        data = JSONParser().parse(request)
#        serializer = SensorUbicacionSerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)
