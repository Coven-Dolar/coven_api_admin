from apps.indicadores.models import ValoresMercado, Commodities
import requests


def oro_nacional():
    r = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
    resp = r.json()
    ORO = resp['GOLD']['rate']
    ORO = round(ORO / 28.3495, 2)

    if ORO > 0:
        ValoresMercado.objects.create(
            tipo_mercado='N',
            precio=ORO,
            par='USD/G',
            mercado=Commodities.objects.get(abreviatura='ORO')
        ).save()
