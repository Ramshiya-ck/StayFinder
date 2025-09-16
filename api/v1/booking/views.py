from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from api.v1.booking.serializers import *
from booking.models import *


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from booking.models import Booking
from .serializers import BookingSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_list(request, hotel_id=None):
    user = request.user
    
    bookings = Booking.objects.filter(customer=user)  # ✅ fix

    if hotel_id:
        bookings = bookings.filter(hotel_id=hotel_id)

    serializer = BookingSerializer(bookings, many=True, context={"request": request})
    return Response({
        "status_code": 6000,
        "message": "Booking list retrieved successfully",
        "data": serializer.data
    })




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def booking_create(request, hotel_id):
    data = request.data.copy()
    data["customer"] = request.user.id   # auto-assign logged-in user
    data["hotel"] = hotel_id             # ✅ force hotel_id from URL

    serializer = BookingSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        booking = serializer.save()
        return Response({
            "status_code": 6000,
            "message": f"Booking created successfully for hotel {hotel_id}",
            "data": BookingSerializer(booking, context={"request": request}).data
        })

    return Response({
        "status_code": 6001,
        "message": "Booking creation failed",
        "data": serializer.errors
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_history(request, hotel_id=None):
    """
    Get booking history for the logged-in user.
    Optional: filter by hotel_id or by status (?status=pending/paid/etc)
    """
    user = request.user

    # ✅ Filter bookings by user
    bookings = Booking.objects.filter(customer=user)

    # ✅ Filter by hotel_id if provided in URL
    if hotel_id:
        bookings = bookings.filter(hotel_id=hotel_id)

    # ✅ Optional status filter from query param
    status = request.GET.get("status")
    if status:
        bookings = bookings.filter(status=status.lower())

    # Serialize bookings
    serializer = BookingSerializer(bookings, many=True, context={"request": request})

    return Response({
        "status_code": 6000 if bookings.exists() else 404,
        "message": "Booking history retrieved successfully" if bookings.exists() else "No bookings found",
        "data": serializer.data
    })