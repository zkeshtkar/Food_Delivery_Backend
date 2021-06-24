from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from accounts.views import RegisterWithEmailView, RegisterWithPhoneView, LogoutAPIView

urlpatterns = [
    path('register/customer', RegisterWithPhoneView.as_view()),
    path('register/manager', RegisterWithEmailView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('login/', obtain_auth_token),

]
