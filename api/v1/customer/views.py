from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404



from user.models import User
from customer.models import *
from customer.models import *
from Hotel.models import *
from api.v1.customer.serializers import *

from django.contrib.auth import authenticate



@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        
        response_data ={
            "status_code": 6000,
            "data": {
                "access": str(refresh.access_token)
            },
            "message": "User Authenticated successfully",
       
        }
        return Response(response_data) 
    else:

        response_data={
            "status_code": 6001,
            "message": "Invalid Credential"

        }
        return Response(response_data)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    email = request.data.get('email')
    password = request.data.get('password')

    print(request.data)

    if User.objects.filter(email=email).exists():
        response_data = {
            "status_code": 6001,
            "data": {
            "message":"email already exist"
            }
        }
        return Response(response_data)
    
    user = User.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = password,
        is_customer = True
    )
    user.save()

    customer = Customer.objects.create(
        user=user
    )

    customer.save()
    refresh = RefreshToken.for_user(user)
    response_data = {
        'status_code' : 6000,
        'data':{
            'access':str(refresh.access_token)
        },
        'message':'user is registerd succssfully'
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context = {
        'request':request
    }
    serializers = CustomerSerializer(customer,context=context)
    response_data = {
        'status_code' : 6000,
        'data' : serializers.data,
        'message' : 'Profile data retrieved successfully'
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_create(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context = {
        'request':request   
    }
    serializers = CustomerSerializer(customer,context= context,data=request.data)
    if serializers.is_valid():
        serializers.save()
        response_data = {
            'status_code' : 6000,
            'data' : serializers.data,
            'message' : 'Profile created successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code' : 6001,
            'error' : serializers.errors,
            'message' : 'Profile creation failed'
        }
        return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    context = {
        'request':request   
    }
    serializers = CustomerSerializer(customer,context= context,data=request.data,partial=True)
    if serializers.is_valid():
        serializers.save()
        response_data = {
            'status_code' : 6000,
            'data' : serializers.data,
            'message' : 'Profile updated successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code' : 6001,
            'error' : serializers.errors,
            'message' : 'Profile updation failed'
        }
        return Response(response_data)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def profile_delete(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    customer.delete()
    user.delete()
    response_data = {
        'status_code' : 6000,
        'data' : {},
        'message' : 'Profile deleted successfully'
    }
    return Response(response_data)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    slider = Slider.objects.all()
    hotel = Hotal.objects.all()
    context = {
        'request':request
    }
    slider_serializers = SliderSerializer(slider,many=True,context=context)
    hotel_serializers = HotelSerializer(hotel,many=True,context=context)
    response_data = {
        "status_code": 6000,
        "slider": slider_serializers.data,
        "hotel": hotel_serializers.data,
        "message": "Index data retrieved successfully"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def slider(request):
    instance = Slider.objects.all()
    context = {
        'request':request
    }
    serializers = SliderSerializer(instance, many=True, context=context)

    response_data = {
       'status_code' : 6000,
       'data' : serializers.data,
       'message' : 'Slider list retrieved successfully'
    }
    return Response(response_data)



    
    



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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    response_data = {
        "status_code": 6000,
        "message": "Logout successfully"
    }
    return Response(response_data)
    
   






    



    



   








    







        



