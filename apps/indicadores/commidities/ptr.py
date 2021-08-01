import json
import requests
from apps.indicadores.models import ValoresMercado, Commodities


def ptr():
    url = "https://petroapp-price.petro.gob.ve/price/"

    payload = json.dumps({
        "coins": [
            "PTR"
        ],
        "fiats": [
            "USD",
            "BS"
        ]
    })
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'cpid=!7bgnT3uqN8XlWJKrSbeA4Z80Zd7+nRy62AheQHDdkWYc6Z4bZYJ8rAojXpIVN1oKpLNe17Y9UPY/zVg='
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    resp = json.loads(response.text)
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
