from django.contrib import admin
from .models import Run, Like, Comment, Profile, Follow

# Register your models here.
admin.site.register(Run)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Follow)