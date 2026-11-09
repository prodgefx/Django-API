from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Product

@register(Product)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public'
    fields = [
        'title',
        'body',
        'price',
        'user_id',
        'path', 
        'public'
    ]
    settings = {
        'attributesForFaceting': ['user', 'public'],
        'searchableAttributes': ['body', 'title']
    }

    tags = 'get_tags_list'
