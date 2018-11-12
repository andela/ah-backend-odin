import uuid
from rest_framework import generics
from .models import Article
from .serializers import CreateArticleAPIViewSerializer, UpdateArticleAPIVIEWSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .renderers import ArticleJSONRenderer
from django.template.defaultfilters import slugify
from ..authentication.backends import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from ..authentication.models import User
from django.shortcuts import get_object_or_404


class ListCreateArticleAPIView(generics.ListCreateAPIView):


    renderer_classes = (ArticleJSONRenderer, )
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """
            This method creates user articles
        """
        article = request.data.get('article', {})
        user_info = JWTAuthentication().authenticate(request)
        article['author'] = user_info[0]

        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user_info[0])
        data = serializer.data
        data["message"] = "Your Article has been created successfully"

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateDestroyArticleAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class = UpdateArticleAPIVIEWSerializer

    def update(self, request, slug):

        """
            This method updates a user article
        """
        article = request.data.get('article', {})
        user_info = JWTAuthentication().authenticate(request)
        article["author"] = user_info[0].pk
        
        article_instance = get_object_or_404(Article, slug=slug)
        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.update_article(article,article_instance)
        data = serializer.data
        data["message"] = "Article updated successfully."

        return Response(data, status=status.HTTP_201_CREATED)
