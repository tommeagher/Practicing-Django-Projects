from django.conf.urls.defaults import *

from blurg.models import Category

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Category.objects.all() }, 'blurg_category_list'),
    (r'^(?P<slug>[-\w]+)/$', 'blurg.views.category_detail', {}, 'blurg_category_detail'),
)