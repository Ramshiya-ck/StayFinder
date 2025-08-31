from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

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
@permission_classes([AllowAny])
def hotel(request):
    instance = Hotal.objects.all()
    location = request.GET.get('location')
    if location :
        instance = Hotal.objects.filter(location__icontains = location)
    else:
        instance = Hotal.objects.all()
    context = {
        'request':request
    }
    serializers = HotelSerializer(instance, many=True, context=context)

    response_data = {
       'status_code' : 6000,
       'data' : serializers.data,
       'message' : 'Hotel list retrieved successfully'
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_hotel(request,id):
    user = request.user
    customer = Customer.objects.get(user=user)
    instance = Hotal.objects.get(id=id)
    room = Room.objects.filter(hotel=instance)

    context = {
        'request':request
    }


    response_data ={
        'status_code': 6000,
        'Hotel':HotelSerializer(instance,context=context).data,
        'room' :RoomSerializer(room,many = True).data,

        'message': 'Hotel retrived successfully'
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hotel_create(request):
    
    context = {
        'request':request
    }
    serializer = HotelSerializer(data = request.data,context=context)
    if serializer.is_valid():
        serializer.save()
        
        response_data = {
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Hotal created successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code':6001,
            'error':serializer.errors,
            'message':'Hotal creation failed'
        }
        return Response(response_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def hotel_edit(request,id):
    instance = Hotal.objects.get(id=id)
   

    hotal_name = request.data.get('hotal_name')
    image = request.data.get('image')
    description = request.data.get('description')
    phone = request.data.get('phone')
    rating = request.data.get('rating')
    location = request.data.get('location')
    email = request.data.get('email')
    amentities = request.data.get('amentities')
    is_active = request.data.get('is_active')


    instance.hotal_name = hotal_name
    instance.image = image
    instance.description = description
    instance.phone = phone
    instance.rating = rating
    instance.location = location
    instance.email = email
    instance.amentities = amentities
    instance.is_active = is_active
    instance.save()

    response_data = {
        'status_code':6001,
        'message':'Hotal updated success fully'
    }
    return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def hotel_deleted(request, id):
   instance = Hotal.objects.get(id=id)
   instance.delete()

   response_data = {
       "status_code": 6000,
       "data": {},
       "message": "Address deleted successfully"
   }
   return Response(response_data)
    
    

@api_view(['GET'])
@permission_classes([AllowAny])
def rooms(request):
    instance = Room.objects.all()
    room_type = request.GET.get('room_type')
    availability = request.GET.get('availability')

    if room_type:
        queryset = Room.objects.filter(room_type=room_type) 

    if availability is not None:
        if availability.lower() == 'True':
            queryset = queryset.filter(availability=availability)
        elif availability.lower() == 'False':
            queryset = queryset.filter(availability=availability)

    context = {
        'request': request
    }
    serializers = RoomSerializer(instance, many=True, context=context)
    response_data = {
        'status_code': 6000,
        'data' : serializers.data,
        'message' : 'Room list retrived successfully'
    }
    return Response(response_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_create(request):
    context = {
        'request':request
    }
    serializer = RoomSerializer(data = request.data,context=context)
    if serializer.is_valid():
        serializer.save()
        
        response_data = {
            'status_code': 6000,
            'data': serializer.data,
            'message': 'Room created successfully'
        }
        return Response(response_data)
    else:
        response_data = {
            'status_code':6001,
            'error':serializer.errors,
            'message':'Hotal creation failed'
        }
        return Response(response_data)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def room_edit(request,id):
    instance = Room.objects.get(id=id)
   


    image = request.data.get('image')
    hotel = request.data.get('hotel')
    room_type = request.data.get('room_type')
    price = request.data.get('price')
    availability = request.data.get('availability')
    

    instance.image = image
    instance.hotel = hotel
    instance.room_type = room_type
    instance.price = price
    instance.availability = availability
    
    instance.save()

    response_data = {
        'status_code':6001,
        'message':'Room updated success fully'
    }
    return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def room_deleted(request, id):
   instance = Room.objects.get(id=id)
   instance.delete()

   response_data = {
       "status_code": 6000,
       "data": {},
       "message": "Room deleted successfully"
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
def booking_create(request,id):
    data = request.data
    context = {
        "request" : request
    }
    serializers = BookingSerializer(context=context,data=data)
    if serializers.is_valid():
        serializers.save

        response_data = {
            "status_code" : 6000,
            "data" : serializers.data,
            "message" : 'Booking created successfully'
        }
    
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
    response_data = {
        "status_code": 6001,
        "errors": serializer.errors,
        "message": "Booking update failed"
    }
    return Response(response_data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def booking_deleted(request,id):
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
    booking = Booking.objects.filter(user=user).order_by('-created_at')
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






@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    response_data = {
        "status_code": 6000,
        "message": "Logout successfully"
    }
    return Response(response_data)
    
   






    



    



   








    







        



