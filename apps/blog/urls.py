from django.urls import path

from apps.blog.views import ListadoCategorias, Articulos, ArticulosDetalle, ArticulosCategoria

urlpatterns = [
    path('category/', ListadoCategorias.as_view()),
    path('post/', Articulos.as_view()),
    path('post/category/<url_category>/', ArticulosCategoria.as_view()),
    path('post/<url_post>', ArticulosDetalle.as_view()),
]