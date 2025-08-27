from django.urls import path
from api.v1.customer import views

urlpatterns=[
    path('login/',views.login ,name='login'),
    path('register/',views.register,name='register'),
    path('hotel/',views.hotel,name='hotel'),
    path('room/',views.rooms,name='room')

]
