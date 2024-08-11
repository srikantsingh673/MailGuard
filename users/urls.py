from django.urls import path
from .views import GenerateOTPView, VerifyOTPView, Logout, UserView

urlpatterns = [
    path('get-otp/', GenerateOTPView.as_view(), name='generate_otp'),
    path('login/', VerifyOTPView.as_view(), name='verify_otp and login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', UserView.as_view(), name='UserView'),
]
