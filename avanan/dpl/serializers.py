from rest_framework import serializers

from avanan.dpl.models import Leak


class LeakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leak
        fields = ["message", "content", "channel", "pattern"]
