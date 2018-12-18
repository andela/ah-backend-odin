from django.urls import path
from . import views
app_name = "profile"

urlpatterns = [
    path("profile/<str:username>", views.ProfileDetails.as_view())
]
