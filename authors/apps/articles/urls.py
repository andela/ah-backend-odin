from django.urls import path
from .views import (
    ListCreateArticleAPIView,
    UpdateDestroyArticleAPIView,
    BookMarkArticleAPIView,
    LikeArticleAPIView, 
    CreateRatings, RetrieveRatings, 
    RetrieveAllArticlesWithRatings

)

urlpatterns = [
    path('', ListCreateArticleAPIView.as_view()),
    path('<slug>', UpdateDestroyArticleAPIView.as_view(), ),
    path('<slug>/bookmark', BookMarkArticleAPIView.as_view(), ),
    path('<slug>/likes', LikeArticleAPIView.as_view(), )
    path('<slug>/ratings/', CreateRatings.as_view()),
    path('<slug>/viewratings/', RetrieveRatings.as_view() ),
    path('ratings/', RetrieveAllArticlesWithRatings.as_view() ),

]
