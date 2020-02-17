from django.urls import path

from apps.indicadores.views import Internacional

urlpatterns = [
    path('mercados/internacionales/', Internacional.as_view())
]