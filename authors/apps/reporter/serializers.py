from rest_framework import serializers

from .models import ReportArticle

class ReportedArticleSerializer(serializers.ModelSerializer):
    # serializer to format the instance to JSON
    
    class Meta: 
        model = ReportArticle
        fields = ('id', 'user', 'reason' ,'article', 'date_reported')