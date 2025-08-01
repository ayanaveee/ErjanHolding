from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('otp_verify/<int:user_id>', views.user_otp_verify, name='otp_verify'),
    path('profile/', views.user_profile, name='profile'),

]

