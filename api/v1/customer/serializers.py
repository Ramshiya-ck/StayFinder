from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from Hotel.models import *
from Room.models import *
from booking.models import *
from user.models import *
from customer.models import *



class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user','phone','address','profile_image','id_proof','nationality']




class SliderSerializer(ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id','name','image','description']       

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['id','image','hotel_id','room_type','price','availability']

class BookingSerializer(ModelSerializer):
    class Meta:
        hotel = serializers.PrimaryKeyRelatedField(queryset=Hotal.objects.all())
        room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

        model = Booking
        fields = ['id','customer','hotel','room','check_in','check_out','number_of_guest','status','created_at','updated_at']



