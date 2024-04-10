from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ProfileDetail, FeedRun,FollowerRunFeed, CreateRun, UserRuns, CommentListCreate, FollowingList, FollowerList, LikeRun

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('profile/<int:user_id>/', ProfileDetail.as_view(), name='profile-detail'),

    #Follower & Following paths
    path('profile/<int:user_id>/followers/', FollowerList.as_view(), name='follower-list'),
    path('profile/<int:user_id>/following/', FollowingList.as_view(), name='following-list'),

    #Run Paths:
    path('runs/feed/', FeedRun.as_view(),name="feed-run"),
    path('runs/feed/followed/', FollowerRunFeed.as_view(), name='followed-run-feed'),
    path('runs/:id/', UserRuns.as_view(), name='user-runs'),
    path('runs/<int:profile_id>/create/', CreateRun.as_view(), name="create-run"),
    
    #Comments 
    path('runs/:id/comment', CommentListCreate.as_view(), name="list-create-comment"),
    #Like Path?
    path('runs/<int:run_id>/like/', LikeRun.as_view(), name='like-run'),
]
