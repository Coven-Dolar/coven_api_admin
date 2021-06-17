from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blog.models import Categorias, Post
from apps.blog.serializers import CategoriasSerializers, PostSerializers


class ListadoCategorias(ListAPIView):
    serializer_class = CategoriasSerializers
    queryset = Categorias.objects.filter(status=True)

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class Articulos(ListAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.filter(activo=True)

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ArticulosRecientes(ListAPIView):
    serializer_class = PostSerializers
    queryset = Post.objects.filter(activo=True)[:6]

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ArticulosCategoria(ListAPIView):
    serializer_class = PostSerializers

    def get_queryset(self):
        return Post.objects.filter(categoria__url=self.kwargs['url_category'])

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ArticulosDetalle(APIView):
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request, url_post):
        datos = Post.objects.get(url=url_post)
        serializer = PostSerializers(datos)
        return Response(serializer.data)
