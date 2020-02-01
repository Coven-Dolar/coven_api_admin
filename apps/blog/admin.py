from django.contrib import admin
from django.utils.datastructures import MultiValueDictKeyError
from .models import Categorias, Post
from django.contrib.auth.models import User

# Register your models here.
from .utils.File import File


class AdminCategorias(admin.ModelAdmin):
    list_filter = ('status',)
    fieldsets = [
         (None, { 'fields': ['categoria', 'status'] }),
         ]
    list_display = ('categoria', 'url','total_articulos')


admin.site.register(Categorias, AdminCategorias)

class AdminPost(admin.ModelAdmin):
    list_filter = ('usuario','categoria', 'activo')
    fieldsets = [
        (None, {'fields': [('titulo', 'foto_principal')]}),
        (None, {'fields': [('categoria', 'activo')]}),
        (None, {'fields': ['resumen']}),
        (None,{'fields': ['descripcion']}),
    ]
    list_display = ('titulo', 'url', 'fecha_creacion', 'cantidad_visitas', 'ultima_lectura',)

    def save_model(self, request, obj, form, change):
        try:
            filex = File(request.FILES['foto_principal'], '', 'images')
            filex.upload()
            obj.foto_principal = str(filex.getFile())
            obj.foto_miniatura = 'images/md_' +filex.getNameEncryp()
        except MultiValueDictKeyError:
            pass
        obj.titulo = request.POST['titulo']
        obj.resumen = request.POST['resumen']
        obj.descripcion = request.POST['descripcion']
        obj.usuario = User.objects.get(id=request.user.id)
        obj.save()

        #sumo 1 post mas a la cantidad de publicados en la categoria
        if not change:
            datos_categoria = Categorias.objects.get(id=request.POST['categoria'])
            cantidad = datos_categoria.total_articulos + 1
            Categorias.objects.filter(id=request.POST['categoria']).update(total_articulos=cantidad)

admin.site.register(Post, AdminPost)
