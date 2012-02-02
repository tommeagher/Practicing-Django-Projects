from django.conf.urls.defaults import *

from blurg.models import Category

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Category.objects.all() }),
    (r'^(?P<slug>[-\w]+)/$', 'blurg.views.category_detail'),
)