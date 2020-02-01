from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Categorias, Post
from apps.blog.serializers import CategoriasSerializers, PostSerializers


class ListadoCategorias(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CategoriasSerializers
    queryset = Categorias.objects.filter(status=True)

class Articulos(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializers
    queryset = Post.objects.filter(activo=True)

class ArticulosCategoria(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializers

    def get_queryset(self):
        return Post.objects.filter(categoria__url=self.kwargs['url_category'])

class ArticulosDetalle(APIView):
    def get(self, request, url_post):
        datos = Post.objects.filter(url=url_post)
        serializer = PostSerializers(datos, many=True)
        return Response(serializer.data)