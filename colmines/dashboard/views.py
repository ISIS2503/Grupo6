from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.parsers import JSONParser
from .models import Ubicacion,Tipo,MicroControlador,Alerta, Medicion,AlertaActuador
from .serializers import UbicacionSerializer,TipoSerializer,MicroControladorSerializer,AlertaSerializer,MedicionSerializer,AlertaActuadorSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.views import login
from django.contrib.auth import authenticate
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import time


def index(request):
  return render(request, 'security/login.html')

def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('dashboard')
    else:
        return login(request)

@login_required
def dashboard(request):
    groups = request.user.groups.values_list('name', flat=True)
    group = None
    micros=MicroControlador.objects.all()
    fueraDeLinea=0
    fueraDeRango=0
    conAlerta=0
    for micro in micros:
        alert=0
        if(micro.estadoGas=="fueraDeLinea"):
            fueraDeLinea+=1
            alert=1
        elif(micro.estadoGas=="fueraDeRango"):
            fueraDeRango+=1
            alert = 1
        if (micro.estadoLuz == "fueraDeLinea"):
            fueraDeLinea += 1
            alert = 1
        elif (micro.estadoLuz == "fueraDeRango"):
            fueraDeRango += 1
            alert = 1
        if (micro.estadoRuido == "fueraDeLinea"):
            fueraDeLinea += 1
            alert = 1
        elif (micro.estadoRuido == "fueraDeRango"):
            fueraDeRango += 1
            alert = 1
        if (micro.estadoTemp == "fueraDeLinea"):
            fueraDeLinea += 1
            alert = 1
        elif (micro.estadoTemp == "fueraDeRango"):
            fueraDeRango += 1
            alert = 1
        conAlerta+=alert

    context={
        'num_micros':len(micros),
        'num_fdr':fueraDeRango,
        'num_fdl': fueraDeLinea,
        'conAlertas': conAlerta
    }
    for g in groups:
        group = g
    if group == 'syso':
        return render(request, 'syso_home.html',context)
    elif group == 'administrador':
        return render(request, 'supervisor_home.html',context)
    else: return render(request, 'base.html')

@login_required
def reportes(request):
    return render(request, 'reportes.html')

@login_required
def alertas(request):
    alertas = Alerta.objects.all()
    paginator = Paginator(alertas, 5)
    page = request.GET.get('page')
    try:
        alertas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        alertas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        alertas = paginator.page(paginator.num_pages)

    context={
        'lista_alertas':alertas
    }
    return render(request, 'alertas.html', context)


@login_required
def actuador(request):
    alertas = AlertaActuador.objects.all()
    paginator = Paginator(alertas, 5)
    page = request.GET.get('page')
    try:
        alertas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        alertas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        alertas = paginator.page(paginator.num_pages)

    context={
        'lista_alertas':alertas
    }
    return render(request, 'alertas_actuador.html', context)

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
        u = data['user']
        del data['user']
        p = data['pw']
        del data['pw']
        user = authenticate(username=u,password=p)

        if user is not None:
            if user.has_perm('dashboard.add_medicion'):
                idData = int((time.time()*1000) % 86400000)
                data['idMedicion']=idData
                serializer = MedicionSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=201)

    return JsonResponse(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','PUT','DELETE'])
def medicion_detail(request, pk, format = None):
    try:
        medicion = Medicion.objects.get(pk=pk)
    except Alerta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MedicionSerializer(medicion)
        return Response(serializer.data)
