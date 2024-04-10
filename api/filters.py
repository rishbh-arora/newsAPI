import django_filters
from .models import News
from django.db.models import Q

class NewsArticleFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_key')
    timestamp = django_filters.DateFromToRangeFilter(field_name='publishedAt')
    source = django_filters.CharFilter(field_name='source', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='icontains')

    def filter_key(self, queryset, name, value):
        keys = value.split()
        query = Q()
        for keyword in keys:
            query |= Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(content__icontains=keyword)
        return queryset.filter(query)

    class Meta:
        model = News
        fields = ['q', 'description', 'author', 'source']
