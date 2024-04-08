from django.contrib import admin
from .models import Run, Geolocation, Like, Comment, Profile

# Register your models here.
admin.site.register(Run)
admin.site.register(Geolocation)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Profile)