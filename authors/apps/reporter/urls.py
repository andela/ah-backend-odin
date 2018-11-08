
from django.urls import path

from .views import ReportingAPIView

urlpatterns = [
    path('<slug>/report/', ReportingAPIView.as_view()),
]