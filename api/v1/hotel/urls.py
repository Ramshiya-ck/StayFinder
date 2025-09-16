 
from django.urls import path
from api.v1.hotel import views


urlpatterns=[
    path('hotel/',views.hotel,name='hotel'),
    path('hotel/create/',views.hotel_create,name='hotel_create'),
    path('hotel/edit/<int:id>/',views.hotel_edit,name='hotel_edit'),
    path('hotel/delete/<int:id>/',views.hotel_deleted,name='hotel_deleted'),
    path('single/hotel/<int:id>/',views.single_hotel,name='hotel'),
    path('hotel/search/',views.hotel_search,name='hotel_search'),

]