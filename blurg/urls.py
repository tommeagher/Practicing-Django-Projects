from django.conf.urls.defaults import *

from blurg.models import Entry, Link, Category

from tagging.models import Tag

entry_info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'pub_date',
}

link_info_dict = {
    'queryset': Link.objects.all(),
    'date_field': 'pub_date',
    }

urlpatterns = patterns('django.views.generic.date_based',
    #(r'^$', 'blurg.views.entries_index'),
    (r'^$', 'archive_index', entry_info_dict, 'blurg_entry_archive_index'),
    (r'^(?P<year>\d{4})/$', 'archive_year', entry_info_dict, 'blurg_entry_archive_year'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', entry_info_dict, 'blurg_entry_archive_month'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', entry_info_dict, 'blurg_entry_archive_day'),
    #(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'blurg.views.entry_detail'),
    (r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', entry_info_dict, 'blurg_entry_detail'),    
    (r'^links/$', 'archive_index', link_info_dict, 'blurg_link_archive_index'),
    (r'^links/(?P<year>\d{4})/$', 'archive_year', link_info_dict, 'blurg_link_archive_year'),
    (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_month', link_info_dict, 'blurg_link_archive_month'),
    (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/$', 'archive_day', link_info_dict, 'blurg_link_archive_day'),
    (r'^links/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'object_detail', link_info_dict, 'blurg_link_detail'),
    )

urlspatterns += patterns('',
    (r'^categories/^$', 'django.views.generic.list_detail.object_list', {'queryset': Category.objects.all() }),
    (r'^categories/(?P<slug>[-\w]+)/$', 'coltrane.views.category_detail'),
    )
    
urlpatterns += patterns('',
    (r'^tags/$', 'django.views.generic.list_detail.object_list', ('queryset': Tag.objects.all() }),
    (r'^tags/entries/(?P<tag>[-\w]+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Entry, 'template_name': 'blurg/entries_by_tag.html' }),
    (r'^tags/links/(?P<tag>{-\w}+)/$', 'tagging.views.tagged_object_list', { 'queryset_or_model': Link, 'template_name': 'blurg/links_by_tag.html' }),    
	)
	