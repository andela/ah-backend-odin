import uuid
import json

import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.response import Response
from django.http import HttpResponse
from .filters import FilterArticles
from django.contrib import auth

from .pagination import ArticleLimitOffSetPagination
from ..authentication.backends import JWTAuthentication
from ..authentication.models import User
from .models import Article, BookmarkingArticles
from .renderers import ArticleJSONRenderer
from .serializers import (ArticleDetailSerializer,
                          CreateArticleAPIViewSerializer,
                          UpdateArticleAPIVIEWSerializer,
                          LikeArticleAPIViewSerializer)

class ListCreateArticleAPIView(generics.ListCreateAPIView):

    renderer_classes = (ArticleJSONRenderer, )
    serializer_class = CreateArticleAPIViewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = ArticleLimitOffSetPagination

    def get_queryset(self):
        return FilterArticles.by_request(self.request)

    def create(self, request):
        """This method creates user articles"""

        article = request.data.get('article', {})
        article['author'] = request.user

        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        data = serializer.data
        data["message"] = "Your Article has been created successfully"

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateDestroyArticleAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = UpdateArticleAPIVIEWSerializer
    detailSerializer = ArticleDetailSerializer

    def update(self, request, slug):
        """This method updates a user article"""

        article = request.data.get('article', {})
        article["author"] = request.user.pk

        article_instance = get_object_or_404(Article, slug=slug)
        slug = slugify(article["title"]).replace("_", "-")
        slug = slug + "-" + str(uuid.uuid4()).split("-")[-1]
        article["slug"] = slug

        token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
        author_name = payload['username']
        user = User.objects.filter(username=author_name).first()

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        if article_instance.author != user:
            raise PermissionDenied

        serializer.update_article(article, article_instance)
        data = serializer.data
        data["message"] = "Article updated successfully."

        return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, slug):
        """This method allows a user to delete his article"""

        article_instance = get_object_or_404(Article, slug=slug)
        if article_instance.author != request.user:
            raise PermissionDenied
        self.perform_destroy(article_instance)
        return Response(
            {"message": "Article is deleted"},
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, slug):
        """This method allows a user to retrieve one article"""

        article_instance = get_object_or_404(Article, slug=slug)
        serializer = self.detailSerializer()
        serializer.instance = article_instance
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookMarkArticleAPIView(generics.ListCreateAPIView):

    renderer_classes = (ArticleJSONRenderer, )
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)
    model = BookmarkingArticles

    def post(self, request, slug):

        user = request.user

        article_id = get_object_or_404(Article, slug=slug)

        # Trying to get a bookmark from the table, or create a new one
        bookmark, created = self.model.objects.get_or_create(
            user=user, article_id=article_id)
        # If no new bookmark has been created,
        # Then we believe that the request was to delete the bookmark
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(article_id=article_id).count()
            }),
            content_type="application/json"
        )


class LikeArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeArticleAPIViewSerializer

    def post(self, request, slug):

        """This method allows user to like and dislike an article"""

        like = request.data.get('article', {})

        user_info = JWTAuthentication().authenticate(request)
        like["author"] = user_info[0].pk

        article_instance = get_object_or_404(Article, slug=slug)
        like["article"] = article_instance.pk
        
        serializer = self.serializer_class(data=like)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        if serializer.action_performed == "created":
            action_status = status.HTTP_201_CREATED
        else:
            action_status = status.HTTP_201_CREATED
        return Response(serializer.data, status=action_status)

