from django.urls import path
from api.v1.room import views

urlpatterns=[
    path('rooms/<int:hotel_id>/',views.rooms,name='rooms'),
    path('room/create/',views.room_create,name='room_create'),
    path('room/edit/<int:id>/',views.room_edit,name='room_edit'),
    path('room/delete/<int:id>/',views.room_deleted,name='room_deleted'),
]