from django.urls import path
from api.v1.booking import views

urlpatterns=[

    path('booking/list/<int:hotel_id>/<int:room_id>/',views.booking_list,name='booking_list'),
    path('booking/create/<int:hotel_id>/',views.booking_create,name='booking_create'),
    path('booking/update/<int:booking_id>/',views.booking_update,name='booking_update'),
    path('booking/delete/<int:booking_id>/',views.booking_deleted,name='booking_deleted'),

    # path('booking/history/<int:id>/',views.booking_history,name='booking_history'),
    path('booking/cancel/<int:id>/',views.booking_cancel,name='booking_cancel'),
    path('booking/reschedule/<int:id>/',views.booking_reschedule,name='booking_reschedule'),



    # __________________payment_____________________

    path("create/advance/payment/", views.create_advance_payment, name="create_advance_payment"),

]