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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
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

    datos = estadisticas()
    context=datos

    for g in groups:
        group = g
    if group == 'syso':
        return render(request, 'syso_home.html',context)
    elif group == 'administrador':
        return render(request, 'supervisor_home.html',context)
    else: return render(request, 'base.html')

def estadisticas():
    ubicaciones=Ubicacion.objects.all()
    areas=[]
    niveles=[]
    for ub in ubicaciones:
        if(ub.area not in areas):
            areas.append(ub.area)
        if(ub.nivel not in niveles):
            niveles.append(ub.nivel)
    areas.sort()
    niveles.sort()
    micros = MicroControlador.objects.all()
    fueraDeLinea = 0
    fueraDeRango = 0
    conAlerta = 0
    nAlertasTemp = 0
    nAlertasLuz = 0
    nAlertasGas = 0
    nAlertasRuido = 0
    nAlertas = 0
    for micro in micros:
        alert = 0
        if ("FueraDeLinea" in micro.estadoGas or "fdl" in micro.estadoGas or "fueraDeLinea" in micro.estadoGas):
            fueraDeLinea += 1
            alert = 1
            nAlertasGas += 1
            nAlertas += 1
        elif ("FueraDeRango" in micro.estadoGas or "fdr" in micro.estadoGas or "fueraDeRango" in micro.estadoGas):
            fueraDeRango += 1
            alert = 1
            nAlertasGas += 1
            nAlertas += 1
        if ("FueraDeLinea" in micro.estadoLuz or "fdl" in micro.estadoLuz or "fueraDeLinea" in micro.estadoLuz):
            fueraDeLinea += 1
            alert = 1
            nAlertasLuz += 1
            nAlertas += 1
        elif ("FueraDeRango" in micro.estadoLuz or "fdr" in micro.estadoLuz or "fueraDeRango" in micro.estadoLuz):
            fueraDeRango += 1
            alert = 1
            nAlertasLuz += 1
            nAlertas += 1
        if ("FueraDeLinea" in micro.estadoRuido or "fdl" in micro.estadoRuido or "fueraDeLinea" in micro.estadoRuido):
            nAlertasRuido += 1
            nAlertas += 1
            fueraDeLinea += 1
            alert = 1
        elif ("FueraDeRango" in micro.estadoRuido or "fdr" in micro.estadoRuido or "fueraDeRango" in micro.estadoRuido):
            nAlertasRuido += 1
            nAlertas += 1
            fueraDeRango += 1
            alert = 1
        if ("FueraDeLinea" in micro.estadoTemp or "fdl" in micro.estadoTemp or "fueraDeLinea" in micro.estadoTemp):
            nAlertasTemp += 1
            nAlertas += 1
            fueraDeLinea += 1
            alert = 1
        elif ("FueraDeRango" in micro.estadoTemp or "fdr" in micro.estadoTemp or "fueraDeRango" in micro.estadoTemp):
            nAlertasTemp += 1
            nAlertas += 1
            fueraDeRango += 1
            alert = 1
        conAlerta += alert
    alertasAct = AlertaActuador.objects.all()
    actuadorIneficiente = 0
    actuadorActivado = 0
    for actuador in alertasAct:
        if (actuador.tipoAlerta == "malFuncionamiento"):
            actuadorIneficiente += 1
        elif (actuador.tipoAlerta == "activado"):
            actuadorActivado += 1
    return {
        'num_micros':len(micros),
        'num_fdr': fueraDeRango,
        'num_fdl': fueraDeLinea,
        'conAlertas': conAlerta,
        'num_ineficiente': actuadorIneficiente,
        'num_activados': actuadorActivado,
        'nAlertasTemp': nAlertasTemp,
        'nAlertasLuz': nAlertasLuz,
        'nAlertasGas': nAlertasGas,
        'nAlertasRuido': nAlertasRuido,
        'nAlertas': nAlertas,
        'areas':areas,
        'niveles':niveles
    }

@login_required
def reportes(request):
    mediciones=Medicion.objects.all()
    micros=MicroControlador.objects.all()
    nAlertasTemp=0
    nAlertasLuz=0
    nAlertasGas=0
    nAlertasRuido=0
    nAlertas=0
    for micro in micros:
        if(micro.estadoGas=="FueraDeLinea"):
            nAlertasGas+=1
            nAlertas+=1
        elif(micro.estadoGas=="FueraDeRango"):
            nAlertasGas+=1
            nAlertas+=1
        if (micro.estadoLuz == "FueraDeLinea"):
            nAlertasLuz += 1
            nAlertas+=1
        elif (micro.estadoLuz == "FueraDeRango"):
            nAlertasLuz += 1
            nAlertas+=1
        if (micro.estadoRuido == "FueraDeLinea"):
            nAlertasRuido += 1
            nAlertas+=1
        elif (micro.estadoRuido == "FueraDeRango"):
            nAlertasRuido += 1
            nAlertas+=1
        if (micro.estadoTemp == "FueraDeLinea"):
            nAlertasTemp += 1
            nAlertas+=1
        elif (micro.estadoTemp == "FueraDeRango"):
            nAlertasTemp += 1
            nAlertas+=1
    if(nAlertas==0):
        context={
            "nAlertasTemp":0 ,
            "nAlertasLuz":0,
            "nAlertasGas":0,
            "nAlertasRuido":0,
            "nAlertas":0,
            "list_mediciones":mediciones
        }
    else:
        context={
             "nAlertasTemp":nAlertasTemp,
            "nAlertasLuz":nAlertasLuz,
            "nAlertasGas":nAlertasGas,
            "nAlertasRuido":nAlertasRuido,
            "nAlertas":nAlertas,
            "list_mediciones":mediciones
        }
    datos = estadisticas()
    context={**context, **datos}
    return render(request, 'reportes.html',context)

#retorna todos los microcontroladores y sus valores
def actuales(request):
    micros = MicroControlador.objects.all()
    req_mediciones = Medicion.objects.all()
    mediciones=[]
    for med in req_mediciones:
        mediciones.append(med)
    mediciones.sort(key=lambda x: x.time, reverse=True)
#    paginatorMic = Paginator(micros, 5)
#    page = request.GET.get('page')
 #   try:
  #      micros = paginatorMic.page(page)

#    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
 #       micros = paginatorMic.page(1)

  #  except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
   #     micros = paginatorMic.page(paginatorMic.num_pages)

    lista_completa=[]
    for micro in micros:
        for med in mediciones:
            if med.idMicro==micro.id:
                ubicacion = Ubicacion.objects.get(pk=micro.ubicacion)
                payload={
                    "id":micro.id,
                    "ubicacion":micro.ubicacion,
                    "nivel": ubicacion.nivel,
                    "area": ubicaion.area,
                    "estadoTemp": micro.estadoTemp,
                    "estadoLuz": micro.estadoLuz,
                    "estadoRuido": micro.estadoRuido,
                    "estadoGas":micro.estadoGas,
                    "temperatura": med.temperatura,
                    "gas":med.gas,
                    "luz": med.luz,
                    "ruido": med.sonido
                }
                lista_completa.append(payload)
                break
    print(lista_completa)
    context={
        "lista_completa":lista_completa
    }
    return render(request,'actuales.html',context)

#retorna todos los microcontroladores y sus valores
def actuales(request,nivel,area):
    micros = MicroControlador.objects.all()
    req_mediciones = Medicion.objects.all()
    mediciones=[]
    for med in req_mediciones:
        mediciones.append(med)
    mediciones.sort(key=lambda x: x.time, reverse=True)
#    paginatorMic = Paginator(micros, 5)
#    page = request.GET.get('page')
 #   try:
  #      micros = paginatorMic.page(page)

#    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
 #       micros = paginatorMic.page(1)

  #  except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
   #     micros = paginatorMic.page(paginatorMic.num_pages)

    lista_completa=[]
    for micro in micros:
        for med in mediciones:
            if med.idMicro==micro.id:
                ubicacion=Ubicacion.objects.get(pk=micro.ubicacion)
                if(ubicacion.area==area and ubicacion.nivel==nivel):
                    payload={
                        "id":micro.id,
                        "ubicacion":micro.ubicacion,
                        "nivel":ubicacion.nivel,
                        "area":ubicaion.area,
                        "estadoTemp": micro.estadoTemp,
                        "estadoLuz": micro.estadoLuz,
                        "estadoRuido": micro.estadoRuido,
                        "estadoGas":micro.estadoGas,
                        "temperatura": med.temperatura,
                        "gas":med.gas,
                        "luz": med.luz,
                        "ruido": med.sonido
                    }
                lista_completa.append(payload)
                break
    print(lista_completa)
    context={
        "lista_completa":lista_completa
    }
    return render(request,'actuales.html',context)


def grafica(request, id, tipo):

    context={
        "id":id,
        "tipo":tipo
    }
    datos = estadisticas()
    context={**context, **datos}
    return render(request, 'microDetail.html',context)


def make_plot(request, id, tipo):
    mediciones = Medicion.objects.all()
    listaMediciones = []
    for med in mediciones:
        listaMediciones.append(med)
    medicionesReturn = []
    tiempos = []
    listaMediciones.sort(key=lambda x: x.time, reverse=False)
    print(mediciones)
    for med in listaMediciones:
        if (med.idMicro == int(id)):
            print(med.gas)
            tiempos.append(med.time)
            if (tipo == 'temperatura'):
                medicionesReturn.append(med.temperatura)
            elif (tipo == 'gas'):
                medicionesReturn.append(med.gas)
            elif (tipo == 'sonido'):
                medicionesReturn.append(med.sonido)
            elif (tipo == "luz"):
                medicionesReturn.append(med.luz)

    #axis.bar(xs, ys)
    ejeY = None
    if tipo == "gas":
        ejeY = "Gases (ppm)"
    elif tipo == "luz":
        ejeY = "Iluminación (lux)"
    elif tipo == "ruido":
        ejeY = "Ruido (dB)"
    elif tipo == "temperatura":
        ejeY = "Temperatura (°C)"
    fig = Figure()
    ax = fig.add_subplot(111)
    print(medicionesReturn)
    print("a")
    print(tiempos)
    x = tiempos
    ax.set_xlabel('Time (HH-MM-SS)', fontsize=14)
    y = medicionesReturn
    ax.set_ylabel(ejeY, fontsize=14)
    ax.plot(x, y)

    canvas = FigureCanvas(fig)
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

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
    datos = estadisticas()
    context={**context, **datos}
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
    datos = estadisticas()
    context={**context, **datos}
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
