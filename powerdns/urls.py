"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url (r'^$', 'powerdns.views.list_domains', name='powerdns_list_domains'),
    url (r'^(?P<slug>[-\w]+)/$', 'powerdns.views.domain_records', name='powerdns_domain_records'), 
)