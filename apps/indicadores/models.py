import decimal

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

MERCADO = (
    ('N', 'NACIONAL'),
    ('I', 'INTERNACIONAL'),
)

class Commodities(models.Model):
    abreviatura = models.CharField(max_length=4, primary_key=True, db_index=True, null=False, blank=False)
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
        
class ValoresMercado(models.Model):
    PAR = (
        ('BS/USD', 'BS/USD'),
        ('BS/PTR', 'BS/PTR'),
        ('USD/PTR', 'USD/PTR'),
        ('EUR/PTR', 'EUR/PTR'),
        ('USD/G', 'USD/G'),
        ('USD/T', 'USD/T'),
        ('USD/QQ', 'USD/QQ'),
    )
    precio = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    #precio_venta = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    #precio_compra = models.DecimalField(max_digits=19, decimal_places=2, null=False, blank=False)
    tipo_mercado = models.CharField(max_length=1, choices=MERCADO, default='N')
    par = models.CharField(max_length=20, choices=PAR, null=False, blank=False,)
    fecha = models.DateTimeField(default=timezone.now, )
    movilidad = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    #movilidad_venta = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    #movilidad_compra = models.DecimalField(max_digits=19, decimal_places=2, default=0)
    mercado = models.ForeignKey(Commodities, on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
        if not self.id:
            try:
                datos = ValoresMercado.objects.filter(tipo_mercado=self.tipo_mercado).latest('fecha')
                if self.precio < datos.precio:
                    movilidad = decimal.Decimal((self.precio * 100)) / decimal.Decimal(datos.precio)
                    self.movilidad = movilidad - 100
                else:
                    self.movilidad = decimal.Decimal(self.precio) / decimal.Decimal(datos.precio)
            except ObjectDoesNotExist:
                pass
        
        
            
        '''if self.precio_venta <  datos.precio_venta:
            movilidad_venta = (self.precio_venta * 100) / datos.precio_venta
            self.movilidad_venta  = movilidad_venta - 100
        else:
            self.movilidad_venta  = self.precio_venta / datos.precio_venta

        if self.precio_compra <  datos.precio_compra:
            movilidad_compra = (self.precio_compra * 100) / datos.precio_compra
            self.movilidad_compra  = movilidad_compra - 100
        else:
            self.movilidad_compra  = self.precio_compra / datos.precio_compra'''

        super(ValoresMercado, self).save(*args, **kwargs)
    
    class Meta:
        db_table = 'in_valores_mercado'
        verbose_name_plural = 'Valores de mercado'
        verbose_name = 'Valor de mercado'
        ordering = ['-fecha']


class Deives(models.Model):
    identificador = models.CharField(max_length=20, null=False, blank=False)
    token = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = 'in_celulares'


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