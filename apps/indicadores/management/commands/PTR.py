# !/usr/bin python3
import json
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


class Command(BaseCommand):
    help = "Obtiene el valor del petro"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://sunacrip.gob.ve/wp-json/petro/v1/prices')
        resp = json.loads(r.json())
        ptr = resp['data']['PTR']

        if ptr['BS'] > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=ptr['BS'],
                par='BS/PTR',
                mercado=Commodities.objects.get(abreviatura='PTR')
            ).save()

        if ptr['USD'] > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=ptr['USD'],
                par='USD/PTR',
                mercado=Commodities.objects.get(abreviatura='PTR')
            ).save()
