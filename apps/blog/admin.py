from django.contrib import admin
from django.utils.datastructures import MultiValueDictKeyError
from .models import Categorias, Post
from django.contrib.auth.models import User

# Register your models here.
from .utils.File import File

@admin.register(Categorias)
class AdminCategorias(admin.ModelAdmin):
    icon_name = 'playlist_add_check'
    list_filter = ('status',)
    fieldsets = [
         (None, { 'fields': ['categoria', 'status'] }),
         ]
    list_display = ('categoria', 'url','total_articulos')


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_per_page = 20
    icon_name = 'library_add'
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
            print(obj.foto_miniatura)
        except MultiValueDictKeyError:
            pass
        obj.titulo = request.POST['titulo']
        obj.resumen = request.POST['resumen']
        obj.descripcion = request.POST['descripcion']
        obj.usuario = User.objects.get(id=request.user.id)
        obj.save()

        #sumo 1 post mas a la cantidad de publicados en la categoria
        if not change:
            datos_categoria = Categorias.objects.filter(id=request.POST['categoria'])
            cantidad = int(datos_categoria.count()) + 1
            categoria = Categorias.objects.get(id=request.POST['categoria'])
            categoria.total_articulos = cantidad
            categoria.save()

            # from fcm_django.models import FCMDevice
            # device = FCMDevice.objects.all()
            # device.send_message(title=request.POST['titulo'],
            #                     body=request.POST['resumen'],
            #                     )
