from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Create your models here.

class Run(models.Model):
    distance = models.IntegerField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    timetotal = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Geolocation(models.Model):
    latitude = models.CharField(max_length=200)
    longtitude = models.CharField(max_length=200)
    elevation = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

    def __str__(self):
        return f'Your lat is {self.latitude}, long is {self.longtitude}'

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return self.comment

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)

# class Friends(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE)
#     following = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.follower} is following {self.following}'