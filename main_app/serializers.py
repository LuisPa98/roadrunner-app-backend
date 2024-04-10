from rest_framework import serializers
from .models import Run, Like, Comment, Profile, Follow
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'last_login', 'date_joined')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        return user

class RunSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Run
        fields = '__all__'
        read_only_fields = ('Profile')

class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('Profile', 'Run')

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = '__all__'
        read_only_fields = ('Profile', 'Run')

class FollowSerializer(serializers.ModelSerializer):
    # follower_id = serializers.PrimaryKeyRelatedField(source='follower.user', read_only=True)
    # following_id = serializers.PrimaryKeyRelatedField(source='following.user', read_only=True)
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following')

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    follower = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('follower', 'following', 'username', 'last_name', 'first_name', 'picture', 'user')