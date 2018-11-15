from django.urls import path


from .views import (
    ListCreateArticleAPIView,
    UpdateDestroyArticleAPIView,
    BookMarkArticleAPIView,
)

urlpatterns = [
    path('', ListCreateArticleAPIView.as_view()),
    path('<slug>', UpdateDestroyArticleAPIView.as_view(), ),
    path('<slug>/bookmark', BookMarkArticleAPIView.as_view(), )

]
