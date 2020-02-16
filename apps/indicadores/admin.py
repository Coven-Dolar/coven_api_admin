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
    list_display = ('commoditi', 'precio', 'par', 'mercado', 'movilidad', 'fecha')
    list_filter = ('commoditi', 'mercado', 'par')
    fields = ('commoditi', 'precio', 'mercado', 'par', 'fecha')
    readonly_fields = ('fecha',)