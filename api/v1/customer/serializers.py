from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Hotel.models import *
from Room.models import *

class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotal
        fields = ['id','hotal_name','image','description','location','email','amentities']

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','image','hotel','room_type','price','availability']


