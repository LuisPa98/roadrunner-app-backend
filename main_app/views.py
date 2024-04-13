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
from django.shortcuts import get_object_or_404
from django.http import Http404


# Define the home view
class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the api home route!'}
    return Response(content)

#Retrieves all Users
class UsersListView(generics.ListAPIView):
  serializer_class = ProfileSerializer
  permission_classes = [permissions.IsAuthenticated]
  queryset = Profile.objects.all()

  def get_queryset(self):
    # Retrieve the 'search' parameter from the URL query parameters, defaulting to None if not present.
    query = self.request.query_params.get('search', None)
    if query is not None: 
      return Profile.objects.filter(user__username__icontains = query)  #Will filter through input of the query to get users assosiated with the query.
    return Profile.objects.all() #Returns all users if no query was inputted

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProfileSerializer
  # checks if person is Authenticated to view profile detail
  permission_classes = [permissions.IsAuthenticated]
  lookup_field = 'user_id'

  # gets user from token
  def get_queryset(self):
    user = self.request.user
    return Profile.objects.filter(user=user)

  # Get user_id from URL params
  def get_queryset(self):
    user_id = self.kwargs.get('user_id')
    return Profile.objects.filter(user_id=user_id)

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
      # if user.delete():
      #   return: Response({'error': 'Profile Deleted'}
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
    profile = Profile.objects.get(user=user)
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data,
      'profile': ProfileSerializer(profile).data
    })

class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      profile = Profile.objects.get(user=user)
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data,
        'profile': ProfileSerializer(profile).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    profile = Profile.objects.get(user=user)
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data,
      'profile': ProfileSerializer(profile).data
    })
  

############        RUN VIEWS       ###############

#Creates an instance of a run
class CreateRun(generics.CreateAPIView):
  serializer_class = RunSerializer
  permission_classes = [permissions.IsAuthenticated]


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


################       FOLOWERS VIEWS      #######################

#Will get all the runs from all the followers you follow.
class FollowingRunFeed(generics.ListAPIView):
  serializer_class = RunSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    # Get the Profile instance for the logged-in user
    user_profile = self.request.user.profile

    # Get the profile instances that the user is following
    followed_profiles_ids = Follow.objects.filter(
        follower=user_profile
    ).values_list('following__user', flat=True)  # Assuming 'following' relates to 'Profile'

    # Fetch runs from these followed profiles
    runs = Run.objects.filter(profile__user__in=followed_profiles_ids).order_by('-date')

    return runs

#Followers Views

class CreateFollow(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, follower_profile_id, following_profile_id):
        # Ensure the follower and following profiles are different
        if follower_profile_id == following_profile_id:
            return Response({'error': 'Cannot follow oneself'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            follower = Profile.objects.get(pk=follower_profile_id)
            following = Profile.objects.get(pk=following_profile_id)
        except Profile.DoesNotExist:
            raise Http404

        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        if created:
            return Response({'status': 'User followed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Already following'}, status=status.HTTP_409_CONFLICT)

class RemoveFollow(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, follower_profile_id, following_profile_id):
        follower = Profile.objects.get(pk=follower_profile_id)
        following = Profile.objects.get(pk=following_profile_id)
        follow = Follow.objects.filter(follower=follower, following=following)
        if follow.exists():
            follow.delete()
            return Response({'status': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 'Follow relationship not found'}, status=status.HTTP_404_NOT_FOUND)

class FollowListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, profile_id):
        profile = get_object_or_404(Profile, pk=profile_id)

        # Get the Follow instances where the given profile is the 'following', to find who is following this profile
        follower_profiles = Follow.objects.filter(following=profile).select_related('follower')
        followers = [follow.follower for follow in follower_profiles]

        # Get the Follow instances where the given profile is the 'follower', to find who this profile is following
        followed_profiles = Follow.objects.filter(follower=profile).select_related('following')
        following = [follow.following for follow in followed_profiles]

        # Serialize the data
        profile_serializer = ProfileSerializer(followers, many=True)
        following_serializer = ProfileSerializer(following, many=True)

        # Return the data in the desired format
        return Response({
            'followers': profile_serializer.data,
            'following': following_serializer.data
        })



##########        COMMENT VIEWS         ###########

class CommentListCreate(generics.ListCreateAPIView):
  serializer_class = CommentsSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    run_id = self.kwargs['run_id']
    return Comment.objects.filter(run_id=run_id)

  def perform_create(self, serializer):
    print("Received data for new comment:", self.request.data)  # Debug print
    run_id = self.kwargs['run_id']
    run = Run.objects.get(id=run_id)
    serializer.save(run=run)




############   LIKE VIEWS      ###########

class LikeRun(APIView):
  permission_classes = [permissions.IsAuthenticated]

  # add like 
  def post(self,request,run_id):
    profile = request.user.profile
    run = Run.objects.get(id=run_id)

    #Check if user already liked run by going through Like Model
    if not Like.objects.filter(profile=profile, run=run).exists():
      Like.objects.create(profile=profile, run=run)
      return Response({
                'status': 'Like Added',
                'profile_id': profile.user.id,
                'username': profile.user.username
            }, status=status.HTTP_201_CREATED)
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