from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.conf import settings
from apps.blog.models import Categorias, Post


class CategoriasSerializers(ModelSerializer):

    class Meta:
        model = Categorias
        fields = ['categoria', 'url', 'total_articulos']

class PostSerializers(ModelSerializer):
    usuario = serializers.SlugRelatedField(read_only=True, slug_field='username')
    categoria = serializers.SlugRelatedField(read_only=True, slug_field='url')
    nombre_categoria = serializers.SlugRelatedField(read_only=True, slug_field='categoria')
    foto_principal = serializers.SerializerMethodField()
    foto_miniatura = serializers.SerializerMethodField()

    def get_foto_principal(self, instance):
        foto_principal = instance.foto_principal
        return settings.SITE_URL +'media/'+ str(foto_principal)

    def get_foto_miniatura(self, instance):
        foto_miniatura = instance.foto_miniatura
        return settings.SITE_URL +'media/'+ str(foto_miniatura)

    class Meta:
        model = Post
        exclude = ['ultima_lectura']


