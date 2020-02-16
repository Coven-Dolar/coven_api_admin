from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.blog.models import Categorias, Post


class CategoriasSerializers(ModelSerializer):

    class Meta:
        model = Categorias
        fields = ['categoria', 'url', 'total_articulos']

class PostSerializers(ModelSerializer):
    usuario = serializers.SlugRelatedField(read_only=True, slug_field='username')
    categoria = serializers.SlugRelatedField(read_only=True, slug_field='url')

    class Meta:
        model = Post
        exclude = ['ultima_lectura']


