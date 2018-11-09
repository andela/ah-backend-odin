from django.db import models
from ..authentication.models import User
from datetime import datetime, timedelta

from taggit.managers import TaggableManager


# Create your models here.

class Article(models.Model):


    title = models.CharField(db_index= True, max_length = 255)
    description = models.CharField(db_index=True, max_length = 255)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    published = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
<<<<<<< HEAD
    tags = TaggableManager(blank=True)
=======
    tagList = TaggableManager(blank=True)
>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb
    slug = models.SlugField(max_length=255, unique=True)
    image = models.TextField(null=True, blank=True)

