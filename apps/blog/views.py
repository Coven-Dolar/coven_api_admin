from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Categorias, Post
from apps.blog.serializers import CategoriasSerializers, PostSerializers


class ListadoCategorias(ListAPIView):
    serializer_class = CategoriasSerializers
    queryset = Categorias.objects.filter(status=True)

class Articulos(ListAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.filter(activo=True)

class ArticulosCategoria(ListAPIView):
    serializer_class = PostSerializers

    def get_queryset(self):
        return Post.objects.filter(categoria__url=self.kwargs['url_category'])

class ArticulosDetalle(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, url_post):
        datos = Post.objects.get(url=url_post)
        serializer = PostSerializers(datos)
        return Response(serializer.data)

