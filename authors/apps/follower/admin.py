from django.contrib import admin

# Register your models here.

from authors.apps.follower.models import Follow

admin.site.register(Follow)
