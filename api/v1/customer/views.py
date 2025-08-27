from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from customer.models import Customer
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
            "status_code": 6000,
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
@permission_classes([AllowAny])
def rooms(request):
    instance = Room.objects.all()
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





    



    



   








    







        



