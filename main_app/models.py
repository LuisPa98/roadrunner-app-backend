from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(upload_to='uploads/')
    username = models.CharField(max_length=20)

    def __str__(self):
        return self.username
    # reciever decorater creates profile when registering user(sender=User) reference to User
    @receiver(post_save, sender=User)
    def update_profile_signal(sender,instance, created, **kwargs):
        # creates and saves profile
        if created:
            Profile.objects.create(user=instance, username=instance.username, picture="")
        instance.profile.save()

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='follower_set', on_delete=models.CASCADE)

class Run(models.Model):
    distance = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    timetotal = models.DateTimeField()
    profile = models.ForeignKey(Profile, related_name='runs', on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, related_name='liked_runs', through='Like')

class Like(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Comment(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.profile.username} commented on {self.run}'

class Geolocation(models.Model):
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    elevation = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return f'Your lat is {self.latitude}, long is {self.longitude}'
