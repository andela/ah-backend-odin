from django.urls import path


from .views import (
    UserRetrieveUpdateAPIView,
    RegistrationAPIView,
    LoginAPIView,
    ActivationAPIView,
    ListUserWithProfiles,
    FacebookAPIView,
    GoogleAPIView
)


# def facebook_response(request, *args,**kwargs):
#     return "Successfull"
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    path('users/verify/<uidb64>/<token>',
        ActivationAPIView.as_view(), name='Activation'),
    path('users', ListUserWithProfiles.as_view()),
    path('facebook_login/', FacebookAPIView.as_view()),
    path('google_login/', GoogleAPIView.as_view()),
]
