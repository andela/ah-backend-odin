from rest_framework import views
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from .serializers import  ProfileSerializer
from .renderers import ProfileRenderer
from .models import Profile
from .permissions import UserOwnsProfifle


class ProfileDetails (RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, UserOwnsProfifle,)
    renderer_classes = (ProfileRenderer,)
    queryset = Profile.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
