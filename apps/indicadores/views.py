import datetime

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from apps.indicadores.models import Leyendas, ValoresMercado, ValoresMercadoActual
from apps.indicadores.serializers import LeyendaMercadoSerializer, ValoresMercadoSerializer


class Internacional(APIView):

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT 	nombre, par, precio, movilidad "
                       "FROM in_commodities INNER JOIN in_valores_mercado ON mercado_id = in_commodities.abreviatura "
                       "WHERE tipo_mercado='I' and activo = true and fecha in (SELECT max(fecha) "
                       "from in_valores_mercado where mercado_id = in_commodities.abreviatura and tipo_mercado = 'I')")
        columns = [col[0] for col in cursor.description]

        data = [dict(zip(columns, row))
                for row in cursor.fetchall()
                ]
        return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))


class Internacionalv2(APIView):
    def get(self, request):
        data = ValoresMercadoActual.objects.filter(tipo_mercado='I')
        serializer = ValoresMercadoSerializer(data, many=True)

        return Response(serializer.data)


class Nacionalv2(APIView):
    def get(self, request):
        data = ValoresMercadoActual.objects.filter(tipo_mercado='N')
        serializer = ValoresMercadoSerializer(data, many=True)

        return Response(serializer.data)


class Nacional(APIView):

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT 	nombre, par, precio, movilidad "
                       "FROM in_commodities INNER JOIN in_valores_mercado ON mercado_id = in_commodities.abreviatura "
                       "WHERE tipo_mercado='N' and activo = true and fecha in (SELECT max(fecha) "
                       "from in_valores_mercado where mercado_id = in_commodities.abreviatura and tipo_mercado = 'N')")
        columns = [col[0] for col in cursor.description]

        data = [dict(zip(columns, row))
                for row in cursor.fetchall()
                ]
        return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))


class LeyendaMercado(APIView):

    def get(self, request, leyenda):
        serializer = LeyendaMercadoSerializer(Leyendas.objects.filter(mercado=leyenda), many=True)
        return Response(serializer.data)


class DataMarketGraph(APIView):

    def get(self, request, typemarket, market):
        data = []
        data.append({'date': market, 'value': 'HISTÓRICO ' + market})
        now = datetime.datetime.now()

        after = now - datetime.timedelta(days=int(request.GET['days']))

        var = ValoresMercado.objects.filter(fecha__range=(after, now),
                                            tipo_mercado=typemarket, mercado__nombre=market).order_by('fecha')

        for item in var:
            data.append({'date': item.fecha.strftime("%m-%d %H:%M"), 'value': item.precio})

        return Response(data)


class MarketGraph(APIView):

    def get(self, request, typemarket, market):
        now = datetime.datetime.now()
        after = now - datetime.timedelta(days=int(request.GET['days']))

        cursor = connection.cursor()
        cursor.execute(
            "SELECT round(avg(in_valores_mercado.precio),2) as precio, TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD HH') as date " \
            "FROM in_valores_mercado " \
            "INNER JOIN in_commodities ON (in_valores_mercado.mercado_id = in_commodities.abreviatura) " \
            "WHERE (TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD') BETWEEN '" + str(
                after.strftime("%Y-%m-%d")) + "' AND '" + str(now.strftime("%Y-%m-%d")) + "' AND " \
            "in_commodities.nombre = '" + market + "' AND in_valores_mercado.tipo_mercado = '" + typemarket + "') " \
            "group by TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD HH') ORDER BY 2 asc")


        data = []
        for item in cursor.fetchall():
            data.append({'date': item[1] + ':00', 'value': item[0]})

        return Response(data)
