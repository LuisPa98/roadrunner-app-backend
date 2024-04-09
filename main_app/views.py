from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import RunSerializer, GeolocationSerializer, CommentsSerializer, LikesSerializer, UserSerializer, ProfileSerializer
from .models import Profile, Like, Comment, Geolocation, Run
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
@receiver(post_save, sender=Profile)
def perform_update(sender, instance, created, **kwargs):
  # Only update if the profile already existed
  if not created:  
        # instance of the model being saved
        user = instance.user
        profile_username = instance.username  
        if user.username != profile_username:
            user.username = profile_username
            user.save()
      
  # will delete user and profile when delete
  def perform_destroy(self, instance):
    user = instance.user
    instance.delete()
    user.delete()

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