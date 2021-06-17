from django.urls import path

from apps.indicadores.views import LeyendaMercado, DataMarketGraph, Nacional, Internacional

urlpatterns = [
    path('mercados/internacionales/', Internacional.as_view()),
    path('mercados/nacionales/', Nacional.as_view()),
    path('mercados/leyenda/<leyenda>/', LeyendaMercado.as_view()),
    path('data/<typemarket>/<market>/', DataMarketGraph.as_view()),
]
