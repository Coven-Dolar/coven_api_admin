#!/usr/bin python3
import decimal
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://www.economies.com/commodities/coffee')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="Last site-float")
        print(span.get_text().strip())

        ValoresMercado(
            tipo_mercado='I',
            precio=decimal.Decimal(span.get_text().strip()),
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()

        '''import pycurl
        import certifi
        from io import BytesIO
        import json

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.barchart.com/symbols/KCY00/modules?symbolType=2&symbolCode=FUT&hasOptions=1')
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, certifi.where())
        c.perform()
        c.close()

        body = buffer.getvalue()
        data = json.loads(body)        
        valor = data['overview']['data'][0]['raw']['lastPrice']
        ValoresMercado(
            tipo_mercado='I',
            precio=valor,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()'''
