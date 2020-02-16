from django.contrib import admin

# Register your models here.
from apps.indicadores.models import *

# admin.site.register(Indicadores)

@admin.register(Leyendas)
class AdminLeyendas(admin.ModelAdmin):
    list_display = ('nomenclatura','descripcion')

@admin.register(Commodities)
class AdminCommodities(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'mercado_internacional', 'mercado_nacional')

@admin.register(ValoresMercado)
class AdminValoresMercado(admin.ModelAdmin):
    list_display = ('mercado', 'precio', 'par', 'movilidad', 'fecha', 'tipo_mercado')
    list_filter = ('mercado', 'tipo_mercado', 'par')
    fields = ('mercado', 'precio', 'tipo_mercado', 'par', 'fecha')
    readonly_fields = ('fecha',)