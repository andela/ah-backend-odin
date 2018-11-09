import json

from rest_framework.renderers import JSONRenderer


class ProfileRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, *args, **kwargs):
        """ Renders a profle Response"""

        errors = data.get('errors', None)

        if errors is not None:
            return super(ProfileRenderer, self).render(data)

        return json.dumps({'profile': data})
