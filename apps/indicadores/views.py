from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class Internacional(APIView):

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT 	nombre, par, precio, movilidad "
                                          "FROM in_commodities INNER JOIN in_valores_mercado ON mercado_id = in_commodities.abreviatura "
                                          "WHERE tipo_mercado='I' and fecha in (SELECT max(fecha) from in_valores_mercado where mercado_id = in_commodities.abreviatura)")
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
                                          "WHERE tipo_mercado='N' and fecha in (SELECT max(fecha) from in_valores_mercado where mercado_id = in_commodities.abreviatura)")
        columns = [col[0] for col in cursor.description]

        data = [dict(zip(columns, row))
                for row in cursor.fetchall()
                ]
        return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))