from rest_framework import serializers
from  booking.models import Booking
from Room.models import Room

class BookingSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Booking
        fields = [
            "id", "hotel", "room", "customer",
            "check_in", "check_out", "number_of_guest",
            "status", "payment_status",
            "created_at", "updated_at", "total_amount",
            "image", "address", "phone"
        ]

    def calculate_total_amount(self, room, check_in, check_out, guests):
        nights = (check_out - check_in).days or 1
        return room.price * nights * guests

    def create(self, validated_data):
        room = validated_data["room"]
        check_in = validated_data["check_in"]
        check_out = validated_data["check_out"]
        guests = validated_data.get("number_of_guest", 1)

        total_amount = self.calculate_total_amount(room, check_in, check_out, guests)

        booking = Booking.objects.create(
            **validated_data,
            total_amount=total_amount
        )
        return booking

    def update(self, instance, validated_data):
        # update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # recalc total_amount if related fields updated
        room = validated_data.get("room", instance.room)
        check_in = validated_data.get("check_in", instance.check_in)
        check_out = validated_data.get("check_out", instance.check_out)
        guests = validated_data.get("number_of_guest", instance.number_of_guest)

        instance.total_amount = self.calculate_total_amount(room, check_in, check_out, guests)
        instance.save()
        return instance

