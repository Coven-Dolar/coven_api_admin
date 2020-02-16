#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    # A commands must define handle()
    def handle(self, *args, **options):
        # Dow Jones Commodity Index Coffee
        '''r = requests.get('https://markets.ft.com/data/indices/tearsheet/summary?s=DJCIKC:DJI')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_='mod-ui-data-list__value')
        ValoresMercado(
            tipo_mercado='I',
            precio=span.get_text(),
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()'''
        headers = {'Content-Type': 'application/json',
                   'Connection': 'keep-alive',
                   'Server': 'nginx',
                   'Via': '1.1 a205b777009b4117039d629e4ab51416.cloudfront.net (CloudFront)',
                   'Vary': 'Accept-Encoding',
                   'X-Frame-Options': 'SAMEORIGIN ALLOW-FROM http://info.barchart.com',
                   'Set-Cookie': 'laravel_session=eyJpdiI6IlR2emdqbkkyV1NFcTdVdDh5ZGoxOHc9PSIsInZhbHVlIjoiRXlDYXg3Y1Q3dHFCempEVzVzdTVZZUozbGgzK1BlUXdBMXBaVCtpWDd3d2lYSTcwUlJtWEdmcGVHOGVVTHN0NSIsIm1hYyI6IjY0NDk3MjViNWUwNTBiN2NhNDA1OTVjZjc3NDc4NjU0OTYzMzEwNWZhYmJjYjYxMDI2ZjNhNzhmNTlhOGQ5MTIifQ%3D%3D; expires=Sun, 16-Feb-2020 20:18:52 GMT; Max-Age=7200; path=/; secure; httponly'}

        r = requests.get('https://www.barchart.com/symbols/KCY00/modules?symbolType=2&symbolCode=FUT&hasOptions=1', headers=headers)
        print(r)
        #soup = BeautifulSoup(r.content, 'html.parser')
        #print(soup)
        #span = soup.find(class_='lastNum pid-8832-last')
        #print(span)

