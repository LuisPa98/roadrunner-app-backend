from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to ='uploads/')
    username = models.CharField(max_length=20)
    # follower_user_id = models.ManyToManyField(Profile) 
    # following_user_id = models.ManyToManyField(Profile)

    def __str__(self):
        return self.username

class Run(models.Model):
    distance = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    timetotal = models.DateTimeField()
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Likes(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Comments(models.Model):
    run_id = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    Comment = models.CharField(max_length=50)

    def __str__(self):
        return f' {self.profile_id.username} commented on {self.run_id}'

class Geolocation(models.Model):
    latitude = models.CharField(max_length=200)
    longtitude = models.CharField(max_length=200)
    elevation = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return f'Your lat is {self.latitude}, long is {self.longtitude}'
