from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ProfileDetail, FeedRun,FollowerRunFeed, CreateRun

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('profile/<int:user_id>/', ProfileDetail.as_view(), name='profile-detail'),

    #Run Paths:
    path('runs/feed/', FeedRun.as_view(),name="feed-run")
    path('runs/feed/followed/', FollowerRunFeed.as_view(), name='followed-run-feed'),
    path('runs/:id/', UserRuns.as_view(), name='user-runs')

    path('profile/<int:user_id>/run/', CreateRun.as_view(), name="create-run"),

]