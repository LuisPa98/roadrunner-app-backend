from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ProfileDetail, FeedRun,FollowingRunFeed, CreateRun, UserRuns, CommentListCreate, LikeRun, CreateFollow, RemoveFollow, FollowListView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('users/register/', CreateUserView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
    path('profile/<int:user_id>/', ProfileDetail.as_view(), name='profile-detail'), 

    #Follower & Following paths
    path('profile/<int:profile_id>/follow-list/', FollowListView.as_view(), name='follow-list'),
    path('profile/<int:follower_profile_id>/follow/<int:following_profile_id>/', CreateFollow.as_view(), name='create-follow'),
    path('profile/<int:follower_profile_id>/unfollow/<int:following_profile_id>/', RemoveFollow.as_view(), name='remove-follow'),

    #Run Paths:
    path('runs/feed/', FeedRun.as_view(),name="feed-run"),
    path('runs/feed/following/', FollowingRunFeed.as_view(), name='following-run-feed'),  
    path('runs/<int:profile_id>/', UserRuns.as_view(), name='user-runs'),
    path('runs/<int:profile_id>/create/', CreateRun.as_view(), name="create-run"),
    
    #Comments Path:
    path('runs/<int:run_id>/comment/', CommentListCreate.as_view(), name="list-create-comment"),

    #Like Paths:
    path('runs/<int:run_id>/like/', LikeRun.as_view(), name='like-run'),
]
