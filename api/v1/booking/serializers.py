from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from booking.models import *







class BookingSerializer(ModelSerializer):
    class Meta:
        hotel = serializers.PrimaryKeyRelatedField(queryset=Hotal.objects.all())
        room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

        model = Booking
        fields = ['id','customer','hotel','room','check_in','check_out','number_of_guest','status','created_at','updated_at']