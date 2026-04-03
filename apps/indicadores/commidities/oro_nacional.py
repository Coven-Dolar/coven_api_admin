import re
import requests
from apps.indicadores.models import Commodities, ValoresMercado
from bs4 import BeautifulSoup

URL = "https://www.goldpricedata.com/es/gold-rates/venezuela/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    )
}


def _parse_number(text: str) -> float:
    """
    Convierte textos como:
    '2,213,266.30' -> 2213266.30
    '71,166.12'    -> 71166.12
    """
    cleaned = re.sub(r"[^0-9.,-]", "", text).strip()
    if not cleaned:
        raise ValueError(f"No se pudo parsear número desde: {text!r}")

    # En esta web el formato visible es anglosajón: 2,213,266.30
    cleaned = cleaned.replace(",", "")
    return float(cleaned)


def _get_gold_24k_gram_ves() -> float:
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text("\n", strip=True)

    match = re.search(
        r"([0-9,]+\.\d+)\s+Bolívar soberano de Venezuela por gramo quilates 24",
        text,
        re.IGNORECASE,
    )

    if not match:
        raise ValueError("No se encontró el precio de 24K por gramo.")

    return _parse_number(match.group(1))

def oro_nacional():
    price_24k = _get_gold_24k_gram_ves()
    ValoresMercado.objects.create(
        tipo_mercado='N',
        precio=price_24k,
        par='USD/G',
        mercado=Commodities.objects.get(abreviatura='ORO')
    ).save()