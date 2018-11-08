from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import ReporterJsonRenderer
from .serializers import ReportedArticleSerializer
from .models import ReportArticle

from ..articles.models import Article
from ..authentication.backends import JWTAuthentication


class ReportingAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ReporterJsonRenderer,)
    serializer_class = ReportedArticleSerializer

    def post(self, request, slug):
        
        report = request.data.get('report', {})
        user = JWTAuthentication().authenticate(request)

        report['user'] = user[0].pk
        article = Article.objects.get(slug=slug)

        print(article)
        report['article'] = article.id

        serializer = self.serializer_class(data=report)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

