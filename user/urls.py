from django.urls import path, include
from . import views

urlpatterns = [

    path('user_registration/', views.UserRegistration.as_view(), name='registration'),
    path('user_login/', views.UserLogin.as_view(), name='login'),
    path('user_logout/', views.UserLogout.as_view(), name='logout'),
]