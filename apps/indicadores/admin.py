from django.contrib import admin

# Register your models here.
from apps.indicadores.models import *


# admin.site.register(Indicadores)

@admin.register(Leyendas)
class AdminLeyendas(admin.ModelAdmin):
    icon_name = 'chrome_reader_mode'
    list_display = ('nomenclatura', 'descripcion')
    list_filter = ('mercado',)


@admin.register(Commodities)
class AdminCommodities(admin.ModelAdmin):
    icon_name = 'art_track'
    list_display = ('nombre', 'activo', 'mercado_internacional', 'mercado_nacional')


@admin.register(ValoresMercado)
class AdminValoresMercado(admin.ModelAdmin):
    icon_name = 'trending_up'
    list_display = ('mercado', 'precio', 'par', 'movilidad', 'fecha', 'tipo_mercado')
    list_filter = ('mercado', 'tipo_mercado', 'par')
    fields = ('mercado', 'precio', 'tipo_mercado', 'par', 'fecha')
    readonly_fields = ('fecha',)


@admin.register(ValoresMercadoActual)
class AdminValoresMercadoActual(admin.ModelAdmin):
    icon_name = 'update'
    list_display = ('mercado', 'precio', 'par', 'movilidad', 'fecha', 'tipo_mercado')
    list_filter = ['tipo_mercado', 'par']
