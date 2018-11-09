import uuid
<<<<<<< HEAD
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
=======

import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from ..authentication.backends import JWTAuthentication
from ..authentication.models import User
from .models import Article
from .renderers import ArticleJSONRenderer
from .serializers import (ArticleDetailSerializer,
                          CreateArticleAPIViewSerializer,
                          UpdateArticleAPIVIEWSerializer)
>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb


class ListCreateArticleAPIView(generics.ListCreateAPIView):


    renderer_classes = (ArticleJSONRenderer, )
    queryset = Article.objects.all()
    serializer_class = CreateArticleAPIViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
<<<<<<< HEAD
        """
            This method creates user articles
        """
=======
        """This method creates user articles"""

>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb
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
<<<<<<< HEAD

    def update(self, request, slug):

        """
            This method updates a user article
        """
=======
    detailSerializer = ArticleDetailSerializer
    

    def update(self, request, slug):

        """This method updates a user article"""

>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb
        article = request.data.get('article', {})
        user_info = JWTAuthentication().authenticate(request)
        article["author"] = user_info[0].pk
        
        article_instance = get_object_or_404(Article, slug=slug)
        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

<<<<<<< HEAD
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
=======
        token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        author_name = payload['username']
        user = User.objects.filter(username=author_name).first()
        
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        if article_instance.author != user:
            raise PermissionDenied
        
>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb
        serializer.update_article(article,article_instance)
        data = serializer.data
        data["message"] = "Article updated successfully."

        return Response(data, status=status.HTTP_201_CREATED)
<<<<<<< HEAD
=======

    def destroy(self, request, slug):
    
        """This method allows a user to delete his article"""

        article_instance = get_object_or_404(Article, slug=slug)
        if article_instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(article_instance)
        return Response({"message": "Article is deleted"}, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):

        """This method allows a user to retrieve one article"""
       
        article_instance = get_object_or_404(Article, slug=slug)
        serializer = self.detailSerializer()
        serializer.instance = article_instance
        return Response(serializer.data, status=status.HTTP_200_OK)
>>>>>>> c0ac52dcb053bc85fb8dc2e92cd627173223d9cb
