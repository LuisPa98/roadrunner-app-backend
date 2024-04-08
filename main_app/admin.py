from django.contrib import admin
from .models import Run, Geolocation, Likes, Comments, Profile

# Register your models here.
admin.site.register(Run)
admin.site.register(Geolocation)
admin.site.register(Likes)
admin.site.register(Comments)
admin.site.register(Profile)