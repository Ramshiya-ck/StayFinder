from django.urls import path
from api.v1.customer import views

urlpatterns=[
    
    path('login/',views.login ,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout ,name='logout'),
    path('profile/',views.profile,name='profile'),

    path('index/',views.index,name='index'),
    path('slider/',views.slider,name='slider'),

   

  

    path('booking/list/',views.booking_list,name='booking_list'),
    path('booking/create/',views.booking_create,name='booking_create'),
    path('booking/update/<int:id>/',views.booking_update,name='booking_update'),
    path('booking/delete/<int:id>/',views.booking_deleted,name='booking_deleted'),

    path('booking/history/<int:id>/',views.booking_history,name='booking_history'),
    path('booking/cancel/<int:id>/',views.booking_cancel,name='booking_cancel'),
    path('booking/reschedule/<int:id>/',views.booking_reschedule,name='booking_reschedule'),
]
