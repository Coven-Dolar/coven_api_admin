import re
import requests
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities


def _normalizar_numero_ve(valor: str) -> float:
    """
    Convierte un número en formato venezolano/español a float.
    Ejemplo: '474,0598' -> 474.0598
    """
    valor = valor.strip().replace(".", "").replace(",", ".")
    return float(valor)

def dolar_euro_ve():
    BCV_URL = "https://www.bcv.org.ve/bcv/coleccion-electronica"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }
    
    try:
        response = requests.get(BCV_URL, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        texto = soup.get_text(" ", strip=True)
        patron = re.compile(r"\b(USD|EUR)\b\s*([0-9]{1,3}(?:\.[0-9]{3})*,[0-9]+|\d+,\d+)")
        coincidencias = patron.findall(texto)

        tasas = {}
        for moneda, valor in coincidencias:
            tasas[moneda] = {
                "valor_original": valor,
                "valor_float": _normalizar_numero_ve(valor),
            }


        if "USD" in tasas:
            ValoresMercado(
                tipo_mercado="N",
                precio=tasas["USD"]["valor_float"],
                par="BS/USD",
                mercado=Commodities.objects.get(abreviatura="USD")
            ).save()

        if "EUR" in tasas:
            ValoresMercado(
                tipo_mercado="N",
                precio=tasas["EUR"]["valor_float"],
                par="BS/EUR",
                mercado=Commodities.objects.get(abreviatura="EUR")
            ).save()


    except Exception as e:
            print(f"Error scraping USD and EUR from bcv: {e}")