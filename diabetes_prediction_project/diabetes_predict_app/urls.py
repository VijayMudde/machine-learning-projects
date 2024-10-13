from django.urls import path,include
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('about_us',views.about_us,name='about_us'),
    path('services',views.services,name='services'),
    path('predict',views.predict,name='predict'),
    path('login/',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('prediction',views.prediction,name='prediction')
    
]