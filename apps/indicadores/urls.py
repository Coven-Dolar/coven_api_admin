from django.urls import path

from apps.indicadores.views import LeyendaMercado, DataMarketGraph, Nacionalv2, Internacionalv2

urlpatterns = [
    path('mercados/internacionales/', Internacionalv2.as_view()),
    path('mercados/nacionales/', Nacionalv2.as_view()),
    path('mercados/leyenda/<leyenda>/', LeyendaMercado.as_view()),
    path('data/<typemarket>/<market>/', DataMarketGraph.as_view()),
]
