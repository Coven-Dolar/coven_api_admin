import os
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
import hashlib
import base64
from PIL import Image


class File:
    __file = ''
    __fileName = ''
    __folder_culter = ''
    mensaje = ''

    def __init__(self, file, fileName, folder_cluster):
        self.__file = file
        self.__fileName = fileName
        self.__folder_culter = folder_cluster + '/'

        '''valida si el director para el cluster que quieren usar esta creado en el sistema '''

        if not os.path.isdir(settings.MEDIA_ROOT + '/' + folder_cluster):
            os.mkdir(settings.MEDIA_ROOT + '/' + folder_cluster)

    def __encrypName(self):
        return hashlib.sha1(str(str(timezone.now())).encode('utf-8')).hexdigest()

    def upload(self):
        if len(self.__fileName) == 0:
            self.__fileName = self.__encrypName()

        try:
            destination = open(settings.MEDIA_ROOT + '/' + self.__folder_culter + self.__fileName + '.png', 'wb+')
            for chunk in self.__file.chunks():
                destination.write(chunk)

            self.setResize(850)
            self.setResize(400, 'md')
            self.setResize(200, 'sm')
            return True

        except (OSError, IOError):
            self.mensaje = _('Disculpe no se logro subir la imagen')

    def getFile(self):
        return self.__folder_culter + self.__fileName + '.png'

    def getNameEncryp(self):
        return self.__fileName + '.png'

    @staticmethod
    def setDeleteFile(fileName):
        photo = settings.MEDIA_ROOT + '/' + fileName
        thumb = fileName.split('/')
        photoThumb = settings.MEDIA_ROOT + '/' + thumb[0] + '/thumb_' + thumb[1]
        try:
            os.remove(photo)
            os.remove(photoThumb)
            return True
        except OSError:
            return False

    def setResize(self, width, name=''):
        origin = settings.MEDIA_ROOT + '/' + self.__folder_culter + self.__fileName + '.png'
        im1 = Image.open(origin)

        wpercent = float(width / im1.size[0])
        hsize = int(im1.size[1] * wpercent)
        img = im1.resize((width, hsize), Image.ANTIALIAS)  # use nearest neighbour

        if name == '':
            new_img = settings.MEDIA_ROOT + '/' + self.__folder_culter + self.__fileName + '.png'
        else:
            new_img = settings.MEDIA_ROOT + '/' + self.__folder_culter + name + '_' + self.__fileName + '.png'
        ext = ".jpg"
        img.save(new_img)
