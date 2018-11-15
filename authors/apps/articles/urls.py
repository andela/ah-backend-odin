from django.urls import path
from .views import (
    ListCreateArticleAPIView,
    UpdateDestroyArticleAPIView,
    BookMarkArticleAPIView,
    LikeArticleAPIView,
)

urlpatterns = [
    path('', ListCreateArticleAPIView.as_view()),
    path('<slug>', UpdateDestroyArticleAPIView.as_view(), ),
    path('<slug>/bookmark', BookMarkArticleAPIView.as_view(), ),
    path('<slug>/likes', LikeArticleAPIView.as_view(), )
]
