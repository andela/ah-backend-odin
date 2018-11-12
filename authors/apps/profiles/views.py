from rest_framework import views
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import parsers
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileAvatarSerializer, ProfileSerializer
from .renderers import ProfileRenderer
from .models import Profile
from .permissions import UserOwnsProfifle


class ProfileBaseView:
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, UserOwnsProfifle,)
    renderer_classes = (ProfileRenderer,)
    queryset = Profile.objects.all()
    lookup_field = 'username'
    lookup_url_kwarg = 'username'


class ProfileAvatar(views.APIView, ProfileBaseView):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = ProfileAvatarSerializer
    permission_classes = (IsAuthenticated, UserOwnsProfifle,)
    renderer_classes = (ProfileRenderer,)

    def put(self, request, username):
        data = dict(image=request.FILES.get("image"))
        serializer = self.serializer_class(
            instance=Profile.objects.get(username=username),
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileDetails(ProfileBaseView, RetrieveUpdateAPIView):
    pass
