from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import isAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

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
    else:

        response_data={
            "status_code": 6001,
            "message": "Invalid Credential"

        }

        return Response(response_data)
    
    @api_view('POST')
    @permission_classes([AllowAny])
    def register(request):
        


        



