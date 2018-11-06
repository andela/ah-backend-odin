from django.urls import path


from .views import (
    ListCreateArticleAPIView,
)

urlpatterns = [
    path('', ListCreateArticleAPIView.as_view()),

]
