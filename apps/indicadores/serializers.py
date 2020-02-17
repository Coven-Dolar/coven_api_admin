from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from apps.indicadores.models import ValoresMercado

class MercadosSerializers(Serializer):
    precio = serializers.DecimalField(max_digits=19, decimal_places=2)
    par = serializers.CharField(max_length=20)
    movilidad = serializers.DecimalField(max_digits=19, decimal_places=2)