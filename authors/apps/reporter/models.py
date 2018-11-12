from django.db import models

from ..authentication.models import User
from ..articles.models import Article

# Create your models here.

class ReportArticle(models.Model):
    # this is the model responsible for creating articles
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(db_index=True, max_length=500)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)

    