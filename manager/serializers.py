from requets.models import Requet
from rest_framework import serializers

class ReclamationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requet 
        fields = ["pk",]


