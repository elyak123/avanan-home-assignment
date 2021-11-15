from rest_framework import viewsets
from rest_framework import permissions

from avanan.dpl import models
from avanan.dpl import serializers


class APILeakViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = models.Leak.objects.all()
    serializer_class = serializers.LeakSerializer
