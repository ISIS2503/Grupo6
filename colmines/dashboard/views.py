from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from dashboard.models import Ubicacion,Tipo,MicroControlador,Alerta, Medicion,AlertaActuador
from dashboard.serializers import UbicacionSerializer,TipoSerializer,MicroControladorSerializer,AlertaSerializer,MedicionSerializer,AlertaActuadorSerializer
from django.template.context_processors import request
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import time


def index(request):
    context = {

    }
    return render(request, 'dashboard/index.html', context)
@api_view(['GET','POST'])
def ubicacion_list(request, format = None):
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

@api_view(['GET','PUT','DELETE'])
def ubicacion_detail(request, pk, format = None):
    try:
        ubicacion = Ubicacion.objects.get(pk=pk)
    except Ubicacion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UbicacionSerializer(ubicacion)
        return Response(serializer.data)

@api_view(['GET','POST'])
def tipo_list(request, format = None):
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

@api_view(['GET','PUT','DELETE'])
def tipo_detail(request, pk, format = None):
    try:
        tipo = Tipo.objects.get(pk=pk)
    except Tipo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TipoSerializer(tipo)
        return Response(serializer.data)


@api_view(['GET','POST'])
def micro_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = MicroControlador.objects.all()
        serializer = MicroControladorSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MicroControladorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET','PUT','DELETE', 'POST'])
def micro_detail(request, pk, format = None):
    try:
        micro = MicroControlador.objects.get(pk=pk)
    except MicroControlador.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MicroControladorSerializer(micro)
        return Response(serializer.data)

    elif request.method == 'PUT':
        valor = request.data

        for v in valor.keys():
            micro.setEstado(v,valor[v])
        microDick = {"id": micro.id, "ubicacion": micro.ubicacion,
                     "estadoTemp": micro.estadoTemp, "estadoGas": micro.estadoGas, "estadoRuido": micro.estadoRuido,
                     "estadoLuz": micro.estadoLuz}
        serializer = MicroControladorSerializer(data=microDick)
        if serializer.is_valid():
            serializer.save()
            return Response(micro)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def alerta_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        alerta = Alerta.objects.all()
        serializer = AlertaSerializer(alerta, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        idData = int((time.time()*1000) % 86400000)
        data['idAlerta']=idData
        serializer = AlertaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET','PUT','DELETE'])
def alerta_detail(request, pk, format = None):
    try:
        alerta = Alerta.objects.get(pk=pk)
    except Alerta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlertaSerializer(alerta)
        return Response(serializer.data)

@api_view(['GET','POST'])
def alertaAct_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        alerta = AlertaActuador.objects.all()
        serializer = AlertaActuadorSerializer(alerta, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        idData = int((time.time()*1000) % 86400000)
        data['idAlerta']=idData
        serializer = AlertaActuadorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET','PUT','DELETE'])
def alertaAct_detail(request, pk, format = None):
    try:
        alerta = AlertaActuador.objects.get(pk=pk)
    except Alerta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlertaActuadorSerializer(alerta)
        return Response(serializer.data)

@api_view(['GET','POST'])
def medicion_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        medicion = Medicion.objects.all()
        serializer = MedicionSerializer(medicion, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        idData = int((time.time()*1000) % 86400000)
        data['idMedicion']=idData
        serializer = MedicionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET','PUT','DELETE'])
def medicion_detail(request, pk, format = None):
    try:
        medicion = Medicion.objects.get(pk=pk)
    except Alerta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicionSerializer(medicion)
        return Response(serializer.data)
