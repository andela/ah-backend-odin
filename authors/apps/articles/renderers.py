import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList



class ArticleJSONRenderer(JSONRenderer):
    
    charset = 'utf-8'
    db_object_label = 'object'
    
    def render (self, data, media_type=None, renderer_context=None):

        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return super(ArticleJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.db_object_label: data
            })
        
        return json.dumps({
            'article' : data
        })


class CommentJsonRenderer(JSONRenderer):
    
    charset = 'utf-8'
    db_object_label = 'Comment'
    
    def render (self, data, media_type=None, renderer_context=None):

        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return super(CommentJsonRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.db_object_label: data
            })
        
        return json.dumps({
            'comment' : data
        })  

class ThreadJsonRenderer(JSONRenderer):
    
    charset = 'utf-8'
    db_object_label = 'Comment'
    
    def render (self, data, media_type=None, renderer_context=None):

        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return super(ThreadJsonRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.db_object_label: data
            })
        
        return json.dumps({
            'comment' : data
        })    

class BookMarkJSONRenderer(JSONRenderer):
    
    charset = 'utf-8'
    db_object_label = 'object'
    
    def render (self, data, media_type=None, renderer_context=None):

        if type(data) != ReturnList:
            errors = data.get('errors', None)

            if errors is not None:
                return super(BookMarkJSONRenderer, self).render(data)

        if type(data) == ReturnDict:
            return json.dumps({
                self.db_object_label: data
            })
        
        return json.dumps({
            'Bookmark' : data
        })