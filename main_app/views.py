from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RunSerializer, CommentsSerializer, LikesSerializer, UserSerializer, ProfileSerializer, FollowSerializer
from .models import Profile, Like, Comment, Run, Follow
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the api home route!'}
    return Response(content)

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProfileSerializer
  # checks if person is Authenticated to view profile detail
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'user_id'

  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)

    return Response(serializer.data)
  # needs to be in patch method
  
  # will delete user and profile when delete
  def perform_destroy(self, instance):
    user = instance.user
    instance.delete()
    user.delete()

@receiver(post_save, sender=Profile)
def perform_update(sender, instance, created, **kwargs):
  # Only update if the profile already existed
  if not created:  
        # instance of the model being saved
        user = instance.user
        profile_first_name = instance.first_name
        profile_last_name = instance.last_name
        profile_username = instance.username  
        if user.username != profile_username:
            user.username = profile_username
            user.first_name = profile_first_name
            user.last_name = profile_last_name
            user.save()
      
class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    })



#Creates an instance of a run
class CreateRun(generics.CreateAPIView):
  serializer_class = RunSerializer

  def perform_create(self, serializer):
      profile_id = self.kwargs['profile_id']
      profile = Profile.objects.get(pk=profile_id)
      print(profile_id)
      print(profile)  # Get the profile instance using profile_id
      serializer.save(profile=profile)

#Gets all runs from the user
class UserRuns(generics.ListAPIView):
  serializer_class = RunSerializer
  lookup_field = 'profile_id'

  def get_queryset(self):
    profile = self.kwargs['profile_id']
    return Run.objects.filter(profile = profile).order_by('-date')


#Will get all the runs from all the users of the app
class FeedRun(generics.ListAPIView):
  serializer_class = RunSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Run.objects.all().order_by('-date')


#Will get all the runs from all the followers you follow.
class FollowerRunFeed(generics.ListAPIView):
  serializer_class = RunSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    #Gets User
    user = self.request.user.profile

    # Get the profiles the user is following
    followers_id = Profile.objects.filter(following_set__follower=user_profile).values_list('id')

    # Fetch runs from these followed profiles
    runs = Run.objects.filter(profile_id__in=followed_profiles_ids).order_by('-date')

    return runs

#Followers Views

class FollowDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = FollowSerializer

  def follow_user(request):
    follower_profile_id = request.POST.get('follower_profile_id')
    following_profile_id = request.POST.get('following_profile_id')
    Follow.objects.create(follower=follower_profile_id, following=following_profile_id)
    return Response({'success': 'User followed successfully'})
  
  def unfollow_user(request):
    follower_profile_id = request.POST.get('follower_profile_id')
    following_profile_id = request.POST.get('following_profile_id')
    Follow.objects.delete()
    return Response({'success': 'User unfollowed successfully'})

class FollowerList(generics.ListAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
      profile = self.request.user.profile
      return profile.follower.all()

class FollowingList(generics.ListAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    profile = self.request.user.profile
    return profile.following.all()

class CommentListCreate(generics.ListCreateAPIView):
  serializer_class = CommentsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    run_id = self.kwargs['run_id']
    return Comment.objects.filter(run_id=run_id)

  def perform_create(self, serializer):
    run_id = self.kwargs['run_id']
    run = Run.objects.get(id=cat_id)
    serializer.save(run=run)

############   LIKE VIEWS      ###########

class LikeRun(APIView):
  permission_classes = [permissions.IsAuthenticated]

  # add like 
  def post(self,request,run_id):
    profile = request.user.profile
    run, created = Run.objects.get(id=run_id)

    #Check if user already liked run by going through Like Model
    if not Like.objects.filter(profile=profile, run=run).exists():
      Like.objects.create(profile=profile, run=run)
      return Response({'status': 'Like Added'}, status=status.HTTP_201_CREATED)
    else:
      return Response({'status': 'User Already Liked'}, status=status.HTTP_400_BAD_REQUEST)


  # remove like
  def delete(self,request,run_id):
    profile = request.user.profile
    run = Run.objects.get(id=run_id)
    like = Like.objects.filter(profile=profile, run=run)

    if like.exists():
      like.delete()
      return Response({'status': 'Like Removed'}, status=status.HTTP_204_NO_CONTENT)