from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from apps.indicadores.models import Leyendas
from apps.indicadores.serializers import LeyendaMercadoSerializer


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

class Nacional(APIView):

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT 	nombre, par, precio, movilidad "
                                          "FROM in_commodities INNER JOIN in_valores_mercado ON mercado_id = in_commodities.abreviatura "
                                          "WHERE tipo_mercado='N' and fecha in (SELECT max(fecha) "
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

