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
            { 'document_root': '/Users/admin/.virtualenvs/uc/lib/tinymce/jscripts/tiny_mce/'}),
    url(r'^search/$', 'ultracasual.search.views.search'),
    url(r'^list/$', 'ultracasual.search.views.listpages'),
    url(r'', include('django.contrib.flatpages.urls')),
    
)
