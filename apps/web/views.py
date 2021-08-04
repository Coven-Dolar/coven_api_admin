from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from fcm_django.api.rest_framework import AuthorizedMixin, FCMDeviceSerializer, DeviceViewSetMixin
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from fcm_django.settings import FCM_DJANGO_SETTINGS as SETTINGS


class Policy(TemplateView):
    template_name = 'web/policy.html'


class DeviceView(DeviceViewSetMixin):
    def create(self, request, *args, **kwargs):
        serializer = None
        is_update = False
        if (
                SETTINGS.get("UPDATE_ON_DUPLICATE_REG_ID")
                and "registration_id" in request.data
        ):
            instance = self.queryset.model.objects.filter(
                registration_id=request.data["registration_id"]
            ).first()
            if instance:
                serializer = self.get_serializer(instance, data=request.data)
                is_update = True
        if not serializer:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        if is_update:
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            self.subscription(serializer.data['id'])
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

    def subscription(self, id):
        device = FCMDevice.objects.get(id=id)
        device.handle_topic_subscription(True, topic="COVEN-NEWS")
        print('News')


class FCMDeviceViewSet(DeviceView, ModelViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = FCMDeviceSerializer


class FCMDeviceAPI(AuthorizedMixin, FCMDeviceViewSet):
    pass
