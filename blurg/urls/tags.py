from django.conf.urls.defaults import *

from blurg.models import Entry, Link
from tagging.models import Tag
    
urlpatterns = patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Tag.objects.all(), 'template_name': 'blurg/tag_list.html'}, 'blurg_tag_list'),
    (r'^entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Entry.live.all(), 'template_name': 'blurg/entries_by_tag.html' }),
    (r'^links/(?P<tag>{-\w}+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Link, 'template_name': 'blurg/links_by_tag.html' }),    
    #url(r'^(?P<tag>[^/]+)/$', 'blurg.views.tag_detail', 'template_name'='blurg/tag_detail.html'),
)
	