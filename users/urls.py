from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', Register.as_view(), name='register'),
]