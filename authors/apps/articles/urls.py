from django.urls import path


from .views import (
    ListCreateArticleAPIView,
    UpdateDestroyArticleAPIView,
)

urlpatterns = [
    path('', ListCreateArticleAPIView.as_view()),
    path('<slug>', UpdateDestroyArticleAPIView.as_view(), )
]
