import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from authors.apps.profiles.models import Profile


class FollowerJsonRenderer(JSONRenderer):

    charset = 'utf-8'
    db_object_label = 'follower'
    

    def render(self, data, media_type=None, render_context=None):
        
        return json.dumps({
            'follower' : data
        })