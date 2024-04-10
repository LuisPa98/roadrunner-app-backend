from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(upload_to='uploads/', blank=True)
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username
    
    def count_followers(self):
        return self.followers.count()

    def count_followings(self):
        return self.followings.count()
    # reciever decorater creates profile when registering user(sender=User) reference to User model
    @receiver(post_save, sender=User)
    def update_profile_signal(sender,instance, created, **kwargs):
        # creates and saves profile created comes from post_save 
        if created:
            Profile.objects.create(user=instance, username=instance.username, picture="", last_name=instance.last_name, first_name=instance.first_name)
        instance.profile.save()

class Follow(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower_set', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following_set', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

class Run(models.Model):
    distance = models.FloatField()
    date = models.DateField(default=date.today)
    timetotal = models.IntegerField()
    path = models.CharField()
    profile = models.ForeignKey(Profile, related_name='runs', on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile, related_name='liked_runs', through='Like', blank=True)
    comments = models.ManyToManyField(Profile, related_name='comment_runs', through='Comment', blank=True)

    def __str__(self):
        return f'Distance: {distance}, Time Total: {timetotal}'
    
    # Returns the count of likes for this run instance
    def count_likes(self):
        return self.likes.count()

    def count_comment(self):
        return self.comments.count()


class Like(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class Comment(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.CharField(max_length=5000)

    def __str__(self):
        return f'{self.profile.username} commented on {self.run}'


