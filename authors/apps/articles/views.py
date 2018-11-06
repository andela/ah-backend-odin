import uuid
from rest_framework import generics
from .models import Article
from .serializers import CreateArticleAPIViewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .renderers import ArticleJSONRenderer
from django.template.defaultfilters import slugify
from ..authentication.backends import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status


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

        return Response(data, status=status.HTTP_201_CREATED)