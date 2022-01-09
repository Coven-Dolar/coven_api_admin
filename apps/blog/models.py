import requests
import json
from django.conf import settings
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.template import defaultfilters
from django.utils import timezone


# Create your models here.

class Categorias(models.Model):
    STATUS = (
        ('A', 'Habilitado'),
        ('I', 'Inhabilitado'),
    )
    categoria = models.CharField(max_length=60, verbose_name='Nombre Categoria', db_index=True, unique=True, null=False,
                                 blank=False)
    url = models.CharField(max_length=120, verbose_name='Url de la Categoria', null=True, blank=True, db_index=True)
    total_articulos = models.IntegerField(default=0, verbose_name='Cantidad de articulos')
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = defaultfilters.slugify(self.categoria)
            super(Categorias, self).save(*args, **kwargs)
        else:
            super(Categorias, self).save(*args, **kwargs)

    class Meta:
        db_table = 'blog_categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.categoria


class Post(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    STATUS = (
        (ACTIVO, 'Habilitado'),
        (INACTIVO, 'Inhabilitado'),
    )
    titulo = models.CharField(max_length=120, unique=True, verbose_name='Titulo Articulo')
    url = models.CharField(max_length=240, verbose_name='Url', db_index=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False, verbose_name='Fecha de creacion')
    descripcion = RichTextUploadingField(null=False, blank=False)
    resumen = models.TextField(max_length=800, null=True, blank=True, verbose_name='Resumen')
    ultima_lectura = models.DateTimeField(
        editable=False,
        verbose_name='Ultima lectura',
        null=True,
        blank=True,
        auto_now=True
    )
    foto_principal = models.FileField(upload_to='documents/')
    foto_miniatura = models.CharField(max_length=200, null=False, blank=False)
    activo = models.BooleanField(default=True)
    cantidad_visitas = models.IntegerField(default=0, verbose_name='Cantidad de Visitas')
    usuario = models.ForeignKey(User, related_name='pk_usuario_post', on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, related_name='pk_categoria_post', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.url = defaultfilters.slugify(self.titulo)

            url = "https://onesignal.com/api/v1/notifications"

            payload = json.dumps({
                "app_id": settings.ONE_SIGNAL_APP,
                "included_segments": [
                    "Subscribed Users"
                ],
                "data": {
                    "url": self.url
                },
                "headings": {
                    "en": self.titulo
                },
                "contents": {
                    "en": self.resumen
                }
            })

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + settings.ONE_SIGNAL_AUTH
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            super(Post, self).save(*args, **kwargs)
        else:
            super(Post, self).save(*args, **kwargs)

    class Meta:
        db_table = 'blog_post'
        verbose_name = 'Articulo'
        verbose_name_plural = 'Articulos'
        ordering = ['-id']

    def __str__(self):
        return self.titulo
