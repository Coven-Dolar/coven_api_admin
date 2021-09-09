import datetime
from django.db import connection
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.indicadores.models import Leyendas, ValoresMercado, ValoresMercadoActual
from apps.indicadores.serializers import LeyendaMercadoSerializer, ValoresMercadoSerializer


class Internacional(APIView):
    def get(self, request):
        data = ValoresMercadoActual.objects.filter(tipo_mercado='I')
        serializer = ValoresMercadoSerializer(data, many=True)

        return Response(serializer.data)


class Nacional(APIView):
    def get(self, request):
        data = ValoresMercadoActual.objects.filter(tipo_mercado='N')
        serializer = ValoresMercadoSerializer(data, many=True)

        return Response(serializer.data)


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
    @method_decorator(cache_page(60 * 5))
    def get(self, request, typemarket, market):
        now = datetime.datetime.now()
        after = now - datetime.timedelta(days=int(request.GET['days']))

        sql = "SELECT round(avg(in_valores_mercado.precio),2) as precio, TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD HH') as date " \
              "FROM in_valores_mercado " \
              "INNER JOIN in_commodities ON (in_valores_mercado.mercado_id = in_commodities.abreviatura) " \
              "WHERE (TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD') BETWEEN '"+str(after.strftime("%Y-%m-%d"))+"' AND " \
                     "'"+str(now.strftime("%Y-%m-%d"))+"' AND in_commodities.nombre = '" + market + "' AND " \
                     "in_valores_mercado.tipo_mercado = '" + typemarket + "') " \
              "GROUP BY TO_CHAR(in_valores_mercado.fecha, 'YYYY-MM-DD HH') ORDER BY 2 asc"

        cursor = connection.cursor()
        cursor.execute(sql)

        data = []
        for item in cursor.fetchall():
            data.append({'date': item[1] + ':00', 'value': item[0]})

        return Response(data)
