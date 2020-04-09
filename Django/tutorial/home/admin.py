from django.contrib import admin

# Register your models here.
from home.models import Post, Friend

admin.site.register(Post)
admin.site.register(Friend)
