from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.indicadores.models import ValoresMercado
from apps.indicadores.serializers import MercadosSerializers
import json
from django.core import serializers


'''class Internacional(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MercadosSerializers
    queryset = ValoresMercado.objects.filter(tipo_mercado='I').values_list('precio', 'par', 'movilidad').order_by('-fecha')'''


class Internacional(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data = ValoresMercado.objects.filter(tipo_mercado='I', fecha=ValoresMercado.objects.aggregate(max_fecha=Max('fecha')) )\
            .values('precio', 'par', 'mercado__nombre').order_by('-fecha')
        print(data.query)
        #return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))
        return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))