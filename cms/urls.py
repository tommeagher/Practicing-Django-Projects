from django.conf.urls.defaults import patterns, include, url
from coltrane.feeds import LatestEntriesFeed
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = { 'entries': LatestEntriesFeed }


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
    (r'^weblog/categories/', include('coltrane.urls.categories')),
    (r'^weblog/links/', include('coltrane.urls.links')),
    (r'^weblog/tags/', include('coltrane.urls.tags')),
    (r'^weblog/', include('coltrane.urls.entries')),
    (r'^coments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),
    (r'', include('django.contrib.flatpages.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': '/media' }),
    #see how palewire does this with alternates for debugging and not
)