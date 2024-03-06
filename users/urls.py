from django.urls import path, include

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]