from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from Request.models import Request

class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = ["id", '']