from django.urls import path

from .views import FollowingUserAPIView, FollowersUserAPIView, UnFollowingUserAPIView

urlpatterns = [
    path('<username>/follow/', FollowingUserAPIView.as_view()),
    path('<username>/unfollow/', UnFollowingUserAPIView.as_view()),
    path('followers/', FollowersUserAPIView.as_view()),
]