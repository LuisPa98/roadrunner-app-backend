from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ProfileDetail

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('users/<int:profile_id>/', ProfileDetail.as_view(), name='profile-detail')
]