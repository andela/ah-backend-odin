from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import  IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from ..authentication.backends import JWTAuthentication
from authors.apps.profiles.models import Profile
from authors.apps.follower.models import Follow

from .renderers import FollowerJsonRenderer
from .serializers import UserFollowerSerializer, UsersBeingFollowedSerializer, UsersFollowingUserSerializer
from authors.apps.profiles.serializers import ProfileSerializer

# Create your views here.

class FollowingUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerJsonRenderer,)
    serializer_class = UserFollowerSerializer

    def post(self, request, username):

        user = request.user.username
        user_to_follow = Profile.objects.get(username=username)
        user_profile = Profile.objects.get(username=user)
        # follow_instance = Follow.objects.get(username=user, follows=user_to_follow)


        user_data = {"user_following": {"username": str(user),
                                        "follows": str(Follow.objects.filter(username=user_profile).count()),
                                        "following": str(Follow.objects.filter(follows=user_profile).count())},
                    "user_being_followed": {"username": str(user_to_follow.username),
                                            "bio": str(user_to_follow.bio),
                                            "image": str(user_to_follow.image)
                                            } 
                    }
        if user_to_follow.username in Follow.objects.filter(username=user_profile).prefetch_related("follows"):
                user_data["message"] =  "User has already been followed"
        else:
            data = { "username": user_profile,
                        "follows": user_to_follow
                        }
        
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(user_data, status=status.HTTP_201_CREATED)

class UnFollowingUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerJsonRenderer,)

    def delete(self, request, username):

        user = request.user.username
        user_to_unfollow = Profile.objects.get(username=username)
        user_profile = Profile.objects.get(username=user)

        follow_instance = Follow.objects.filter(username=user).filter(follows=user_to_unfollow)

        follow_instance.delete()
        user_data = {"user_following": [{"message": "Unfollow was successful"},
                                        {"username": str(user),
                                        "follows": str(Follow.objects.filter(username=user_profile).count()),
                                        "following": str(Follow.objects.filter(follows=user_profile).count())
                                        }]
                                            }  

        return Response(user_data, status=status.HTTP_200_OK)


class FollowersUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (FollowerJsonRenderer,)
    serializer_class = ProfileSerializer

    def get(self, request):

        user = request.user
        results =  Follow.objects.filter(follows=user.username).prefetch_related("username")
        data=[result.username for result in results]

        serializer = ProfileSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)






