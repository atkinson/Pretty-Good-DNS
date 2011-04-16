from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^django_pdns/', include('django_pdns.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^security/', include('security.urls')),
    
    url (r'^$', 'powerdns.views.list_domains', name='powerdns_list_domains'),
    url (r'^(?P<slug>[-\w]+)/$', 'powerdns.views.domain_records', name='powerdns_domain_records'),

    
    
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
