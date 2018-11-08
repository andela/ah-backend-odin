import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class ReporterJsonRenderer(JSONRenderer):

    charset = 'utf-8'
    db_object_label = 'report'
    

    def render(self, data, media_type=None, render_context=None):
        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return super(ReporterJsonRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.db_object_label: data
            })
    
        return json.dumps({
            'report' : data
        })