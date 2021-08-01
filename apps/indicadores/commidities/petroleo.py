from apps.indicadores.models import ValoresMercado, Commodities
import requests


def petroleo():
    # 45 WTI
    r = requests.get('https://s3.amazonaws.com/oilprice.com/widgets/oilprices/45/last.json')
    resp = r.json()

    if resp['price'] > 0:
        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=resp['price'],
            par='USD/BARRIL',
            mercado=Commodities.objects.get(abreviatura='WTI')
        ).save()

    # 46 BRENT
    r = requests.get('https://s3.amazonaws.com/oilprice.com/widgets/oilprices/46/last.json')
    resp = r.json()

    if resp['price'] > 0:
        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=resp['price'],
            par='USD/BARRIL',
            mercado=Commodities.objects.get(abreviatura='BRENT')
        ).save()
