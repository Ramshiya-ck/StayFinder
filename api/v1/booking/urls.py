from django.urls import path
from api.v1.booking import views

urlpatterns=[

    path('booking/list/',views.booking_list,name='booking_list'),
    path('booking/create/',views.booking_create,name='booking_create'),
    path('booking/update/<int:id>/',views.booking_update,name='booking_update'),
    path('booking/delete/<int:id>/',views.booking_deleted,name='booking_deleted'),

    path('booking/history/<int:id>/',views.booking_history,name='booking_history'),
    path('booking/cancel/<int:id>/',views.booking_cancel,name='booking_cancel'),
    path('booking/reschedule/<int:id>/',views.booking_reschedule,name='booking_reschedule'),

]