#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del WTI petroleo"

    # A commands must define handle()
    def handle(self, *args, **options):
        # 45 WTI
        r = requests.get('https://s3.amazonaws.com/oilprice.com/widgets/oilprices/45/last.json')
        resp = r.json()
        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=resp['price'],
            par='USD/BARRIL',
            mercado=Commodities.objects.get(abreviatura='WTI')
        ).save()

        # 46 BRENT
        r = requests.get('https://s3.amazonaws.com/oilprice.com/widgets/oilprices/46/last.json')
        resp = r.json()
        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=resp['price'],
            par='USD/BARRIL',
            mercado=Commodities.objects.get(abreviatura='BRENT')
        ).save()
