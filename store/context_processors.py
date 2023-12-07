from .models import Category
import logging
from django.core.cache import cache

logger = logging.getLogger('main')


def cats(request):
    logger.info('cats')
    cached_cats = cache.get('cached_cats')

    if cached_cats is None:
        cats = Category.objects.all()
        cache.set('cached_cats', cats, 300)  # Cache for 300 seconds (adjust as needed)
        logger.info('data from db')
    else:
        cats = cached_cats
        logger.info('data from cache')
    return {'cats': cats}