from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Hotel.models import *
from Room.models import *
from booking.models import *


class HotelSerializer(ModelSerializer):
    class Meta:
        model = Hotal
        fields = ['id','hotal_name','image','description','phone','rating','location','email','amentities','is_active']

        

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','image','hotel','room_type','price','availability']

class BookingSerializer(ModelSerializer):
    class Meta:
        hotel = serializers.PrimaryKeyRelatedField(queryset=Hotal.objects.all())
        room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

        model = Booking
        fields = ['id','customer','hotel','room','check_in','check_out','number_of_guest','status','created_at','updated_at']



