from django.urls import path
from api.v1.customer import views

urlpatterns=[
    
    path('login/',views.login ,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout ,name='logout'),
    path('profile/',views.profile,name='profile'),

    path('index/',views.index,name='index'),
    path('slider/',views.slider,name='slider'),

   

  

]
