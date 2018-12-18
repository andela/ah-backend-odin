from django.db.models import Q
from .models import Article


class FilterArticles:
    def __init__(self):
        """ Creates an instance of the FilterArticles class"""
        self.filters = []

    @classmethod
    def by_request(cls, request):
        """ Filters articles by request"""
        return FilterArticles()._run_filters(request.GET)._results().order_by('-updated_at')

    def _run_filters(self, keywords):
        """Runs all the filters available on the request class"""
        for key in keywords:
            self._trigger_filter(key, keywords.get(key))
        return self

    def _trigger_filter(self, filter, value):
        """ Triggers and executes a give filter"""
        filter_method = getattr(self, f"_filter_{filter}", None)
        if filter_method and value:
            filter_method(value)

    def _results(self):
        """ Returns the filtered results"""
        return Article.objects.filter(*self.filters)

    def _filter_title(self, value):
        """ Filters articles by  a given title"""
        self.filters.append(Q(title__icontains=value))

    def _filter_author(self, value):
        """ Filters articles by an author"""
        self.filters.append(
            Q(author__username__icontains=value) |
            Q(author__email__icontains=value)
        )

    def _filter_tag(self, value):
        """ Filters articles by a given tag"""
        self.filters.append(Q(tagList__name__icontains=value))

    def _filter_description(self, value):
        """ Filters articles by a related description"""
        self.filters.append(Q(description__icontains=value))
