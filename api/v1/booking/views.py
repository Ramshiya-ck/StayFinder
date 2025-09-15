from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from api.v1.booking.serializers import *
from booking.models import *




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    instance = Booking.objects.all()
    context = {
        'request' : request
    }
    serializers = BookingSerializer(instance,many = True,context = context)
    response_data = {
        "status_code" : 6000,
        "data" : serializers.data,
        "message"  : 'Booking list retrieved successfully'
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def booking_create(request):
    data = request.data
    context = {
        "request" : request
    }
    serializers = BookingSerializer(context=context,data=data)
    if serializers.is_valid():
        serializers.save()

        response_data = {
            "status_code" : 6000,
            "data" : serializers.data,
            "message" : 'Booking created successfully'
        }
        return Response(response_data)
    
    else:
        response_data = {
            "status_code" : 6001,
            "data" : serializers.errors,
            "message" : 'Booking creation failed'
        }
        return Response(response_data)
    
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def booking_update(request, id):
    booking = Booking.objects.get(id=id)
    data = request.data
    context = {
        "request" : request
    }
    serializer = BookingSerializer(booking, data=data, partial=True, context=context)
    if serializer.is_valid():
        serializer.save()

        response_data = {
            "status_code": 6000,
            "data": serializer.data,
            "message": "Booking updated successfully"
        }
        return Response(response_data)
    
    response_data = {
        "status_code": 6001,
        "errors": serializer.errors,
        "message": "Booking update failed"
    }
    return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def booking_deleted(request,id):
    user = request.user
    instance = Booking.objects.get(id=id)
    instance.delete()

    response_data = {
        "status_code" : 6000,
        "data" : {},
        "message" : "Booking deleted successfully"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_history(request,id):    
    user = request.user
    booking = Booking.objects.filter(customer = id).order_by('-created_at')
    context = {
        "request" : request
    }
    serializers = BookingSerializer(booking,context = context, many = True )
    
    response_data = {
        "status_code" : 6000,
        "data" : serializers.data,
        "message" : 'Booking history retrieved successfully'
    }
    return Response(response_data)


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