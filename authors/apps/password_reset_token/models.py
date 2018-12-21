from django.db import models  # pragma : no cover
from django.utils.timezone import now

# Create your models here.


class Token(models.Model):
    token = models.CharField(
        max_length=140, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)
