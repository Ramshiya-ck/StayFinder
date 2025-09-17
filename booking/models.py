from django.db import models
from user.models import User
from Hotel.models import Hotal
from Room.models import Room 

class Booking(models.Model):

    PAYMENT_STATUS_CHOICES =[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),
        ('completed','Compeleted')

    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed')
    ]

    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotal,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE) 

    address = models.TextField(blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')   

    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ✅ advance payment
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # auto-calculated

    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        db_table = 'booking_list'
        verbose_name = 'booking'
        verbose_name_plural = 'bookings'
        ordering = ['-id']

        def __str__(self):
            return f"Booking #(self.id)-(self.customer)-(self.room.room_type)@(self.hotel.hotal_name)"



