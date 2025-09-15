from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from api.v1.room.serializers import *
from Room.models import *



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rooms(request,hotel_id):   # e.g., /rooms/7/
    rooms = Room.objects.filter(hotel_id=hotel_id)


    print(rooms, "ggggg")

    if not rooms.exists():
        return Response({
            'status_code': 404,
            'data': [],
            'message': 'No rooms found for this hotel'
        })

    serializer = RoomSerializer(rooms, many=True, context={'request': request})
    return Response({
        'status_code': 200,
        'data': serializer.data,
        'message': 'Rooms retrieved successfully'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def room_create(request,hotel_id):
    hotel = Hotal.objects.get(hotel_id=hotel_id)
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
def room_edit(request, id):
    instance = Room.objects.get(id=id)
    hotel_id = request.data.get('hotel')
    if hotel_id:
        
            hotel_instance = Hotal.objects.get(id=int(hotel_id))
            instance.hotel = hotel_instance

            return Response({
                'status_code': 6001,
                'message': 'Invalid hotel id'
            }, status=400)

    if 'image' in request.data:
        instance.image = request.data['image']
    if 'room_type' in request.data:
        instance.room_type = request.data['room_type']
    if 'price' in request.data:
        instance.price = request.data['price']
    if 'availability' in request.data:
        instance.availability = request.data['availability']

    instance.save()

    return Response({
        'status_code': 6000,
        'message': 'Room updated successfully'
    })


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