from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ultracasual.views.home', name='home'),
    # url(r'^ultracasual/', include('ultracasual.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': 'Users/admin/dev/ultracasual/cms/js/tiny_mce/' }),
    url(r'^search/$', 'cms.search.views.search'),
    url(r'^list/$', 'cms.search.views.listpages'),
    url(r'^weblog/$', 'blurg.views.entries_index'),
    url(r'^weblog/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$', 'blurg.views.entry_detail'),
    url(r'', include('django.contrib.flatpages.urls')),
    
)
