# import stripe
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
# stripe.api_key = settings.STRIPE_SECRET_KEY

from api.v1.booking.serializers import *
from booking.models import *


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from booking.models import Booking
from .serializers import BookingSerializer




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_list(request, hotel_id=None, room_id=None):
    customer = request.user

    # Base filter → only customer’s bookings
    bookings = Booking.objects.filter(customer=customer)

    # Optional hotel filter
    if hotel_id:
        bookings = bookings.filter(hotel_id=hotel_id)

    # Optional room filter
    if room_id:
        bookings = bookings.filter(room_id=room_id)

    bookings = bookings.filter(
        advance_amount__gte=(0.3 * models.F("total_amount"))
    )

    serializer = BookingSerializer(bookings, many=True, context={"request": request})
    return Response({
        "status_code": 6000,
        "message": "Booking list retrieved successfully",
        "data": serializer.data
    })







@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_create(request):
    customer = request.user
    hotel_id = request.data.get("hotel")
    room_id = request.data.get("room")
    check_in = request.data.get("check_in")
    check_out = request.data.get("check_out")

    # 🛑 Validation: missing required fields
    if not hotel_id or not room_id or not check_in or not check_out:
        return Response({
            "status_code": 6001,
            "message": "Hotel, Room, Check-in, and Check-out are required"
        })

    # 🛑 Validation: check if room is already booked in date range
    overlapping = Booking.objects.filter(
        hotel_id=hotel_id,
        room_id=room_id,
        booking_status__in=["pending", "confirmed"],  # only active bookings
        check_in__lt=check_out,
        check_out__gt=check_in
    )

    if overlapping.exists():
        return Response({
            "status_code": 6002,
            "message": "This room is already booked for the selected dates"
        })

    # ✅ Create booking
    data = request.data.copy()
    data["customer"] = customer.id
    serializer = BookingSerializer(data=data, context={"request": request})

    if serializer.is_valid():
        serializer.save()
        return Response({
            "status_code": 6000,
            "message": "Booking created successfully",
            "data": serializer.data
        })
    
    return Response({
        "status_code": 6003,
        "message": "Validation failed",
        "errors": serializer.errors
    })

    
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def booking_update(request, booking_id):
    user = request.user

    # ✅ Fetch only bookings of the logged-in user
    bookings = Booking.objects.filter(customer=user, id=booking_id)

    if not bookings.exists():
        return Response({
            "status_code": 6001,
            "message": f"No booking found with ID {booking_id} for this user",
            "data": {}
        })

    booking = bookings.first()
    serializer = BookingSerializer(
        booking, data=request.data, partial=True, context={"request": request}
    )

    if serializer.is_valid():
        updated_booking = serializer.save()
        return Response({
            "status_code": 6000,
            "message": f"Booking {booking_id} updated successfully",
            "data": BookingSerializer(updated_booking, context={"request": request}).data
        })

    return Response({
        "status_code": 6001,
        "message": "Booking update failed",
        "data": serializer.errors
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def booking_deleted(request, booking_id):
    user = request.user

    # ✅ Filter bookings of the logged-in user
    bookings = Booking.objects.filter(customer=user, id=booking_id)
   

    if not bookings.exists():
        return Response({
            "status_code": 6001,
            "message": f"No booking found with ID {booking_id} for this user",
            "data": {}
        })

    booking = bookings.first()
    booking.delete()

    return Response({
        "status_code": 6000,
        "message": f"Booking {booking_id} deleted successfully",
        "data": {}
    })




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def booking_cancel(request,id):
    user = request.user
    instance = Booking.objects.get(id=id)
    instance.status = "cancelled"
    instance.save()

    response_data = {
        "status_code" : 6000,
        "data" : {
            "id" : instance.id,
            "status" : instance.status
        },
        "message" : "Booking cancelled successfully"
    }
    return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def booking_reschedule(request,id):
    user = request.user
    instance = get_object_or_404(Booking, id=id,customer=user)

    check_in = request.data.get('check_in')
    check_out = request.data.get("check_out")
    number_of_guest = request.data.get('number_of_guest')
    status = request.data.get('status')



#  checkout must be after check-in
    if check_out <= check_in:
        response_data = {
            "status_code" : 6001,
            "message" : "Check-out date must be after check-in date."
        }
        return Response(response_data)
    
# Booking must not be cancelled/completed
    if instance.status in ["cancelled", "completed"]:
        response_data = {
            "status_code" : 6001,
            "message" : f"Cannot reschedule a {instance.status} booking."
        }
        return Response(response_data)
    

    
    instance.check_in = check_in
    instance.check_out = check_out
    instance.number_of_guest = number_of_guest

# Only owner/admin should be able to change status
    if status and status in dict(Booking.STATUS_CHOICE).keys():
        instance.status =status
    instance.save()

    response_data = {
        "status_code" : 6000,
        "data" : {
            "id" : instance.id,
            "check_in" : instance.check_in,
            "check_out" : instance.check_out,
            "status" : instance.status,
            "message" : " Booking rescheduled successfully"
        }
    }
    return Response(response_data)

