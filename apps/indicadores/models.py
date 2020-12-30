import decimal

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

MERCADO = (
    ('N', 'NACIONAL'),
    ('I', 'INTERNACIONAL'),
)

PAR = (
    ('BS/USD', 'BS/USD'),
    ('BS/EUR', 'BS/EUR'),
    ('BS/PTR', 'BS/PTR'),
    ('BS/BTC', 'BS/BTC'),
    ('USD/PTR', 'USD/PTR'),
    ('EUR/PTR', 'EUR/PTR'),
    ('USD/G', 'USD/G'),
    ('USD/T', 'USD/T'),
    ('USD/QQ', 'USD/QQ'),
    ('USD/L', 'USD/L'),
    ('USD/L', 'USD/L'),
    ('USD/BARRIL', 'USD/BARRIL'),
    ('USD/BTC', 'USD/BTC'),

)


class Commodities(models.Model):
    abreviatura = models.CharField(max_length=6, primary_key=True, db_index=True, null=False, blank=False)
    nombre = models.CharField(max_length=40, null=False, blank=False)
    mercado_internacional = models.BooleanField(default=True)
    mercado_nacional = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'in_commodities'
        verbose_name_plural = 'Mercados'
        verbose_name = 'Mercado'


class ValoresMercadoActual(models.Model):
    precio = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    tipo_mercado = models.CharField(max_length=1, choices=MERCADO, default='N', db_index=True)
    par = models.CharField(max_length=20, choices=PAR, null=False, blank=False, db_index=True, )
    fecha = models.DateTimeField(default=timezone.now, db_index=True, )
    movilidad = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    mercado = models.ForeignKey(Commodities, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            pass

        ValoresMercadoActual.objects.filter(
            tipo_mercado=self.tipo_mercado,
            par=self.par,
            mercado=self.mercado,
        ).delete()

        super(ValoresMercadoActual, self).save(*args, **kwargs)

    class Meta:
        db_table = 'in_valores_mercado_actual'
        verbose_name_plural = 'Valores de mercado Recientes'
        verbose_name = 'Valor de mercado'
        ordering = ['-fecha']


class ValoresMercado(models.Model):
    precio = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    tipo_mercado = models.CharField(max_length=1, choices=MERCADO, default='N', db_index=True)
    par = models.CharField(max_length=20, choices=PAR, null=False, blank=False, db_index=True, )
    fecha = models.DateTimeField(default=timezone.now, db_index=True, )
    movilidad = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    mercado = models.ForeignKey(Commodities, on_delete=models.CASCADE)

    class Meta:
        db_table = 'in_valores_mercado'
        verbose_name_plural = 'Valores de mercado Historico'
        verbose_name = 'Valor de mercado historico'
        ordering = ['-fecha']

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                datos = ValoresMercado.objects.filter(
                    tipo_mercado=self.tipo_mercado, mercado=self.mercado,
                    par=self.par
                ).latest('fecha')
                if self.precio < datos.precio:
                    movilidad = decimal.Decimal((self.precio * 100)) / decimal.Decimal(datos.precio)
                    self.movilidad = movilidad - 100
                else:
                    self.movilidad = decimal.Decimal(self.precio) / decimal.Decimal(datos.precio)
            except ObjectDoesNotExist:
                pass

        ValoresMercadoActual(
            precio=self.precio,
            tipo_mercado=self.tipo_mercado,
            par=self.par,
            fecha=self.fecha,
            movilidad=self.movilidad,
            mercado=self.mercado,
        ).save()

        super(ValoresMercado, self).save(*args, **kwargs)

    class Meta:
        db_table = 'in_valores_mercado'
        verbose_name_plural = 'Valores de mercado'
        verbose_name = 'Valor de mercado'
        ordering = ['-fecha']


class Leyendas(models.Model):
    nomenclatura = models.CharField(max_length=10, null=False, blank=False)
    descripcion = models.CharField(max_length=100, null=False, blank=False)
    mercado = models.CharField(max_length=1, choices=MERCADO, default='N')

    def __str__(self):
        return self.nomenclatura

    class Meta:
        db_table = 'in_leyendas'
        verbose_name = 'Leyenda de mercado'
        verbose_name_plural = 'Leyendas de mercado'
