from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination)

class ArticleLimitOffSetPagination(LimitOffsetPagination):
    """Implement pagination support for articles"""
    #maximum allowable limit   
    max_limit = 10
