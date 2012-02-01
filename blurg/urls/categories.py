from django.conf.urls.defaults import *

from blurg.models import Category

urlspatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Category.objects.all() }),
    (r'^(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail'),
)