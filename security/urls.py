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
    url(r'^login$', 'security.views.login', {'template_name': 'security/login.html'}, name='security_login'),
    url(r'^logout$','django.contrib.auth.views.logout_then_login', name='security_logout'),
    # url(r'^profile$','authapp.views.profile', name='auth_profile'),
    # url(r'^profile/(?P<uid>[0-9A-Za-z]+)$','authapp.views.profile_edit', name='auth_profile_edit'),
    url(r'^password-reset$', 'security.views.password_reset',  name='security_password_reset'),
    # url(r'^password-reset-done$', 'authapp.views.password_reset_done',  name='auth_password_reset_done'),
    # url(r'^password-reset-confirm/(?P<uid>[0-9A-Za-z]+)-(?P<token>.+)/$', 'authapp.views.password_reset_confirm',  name='auth_password_reset_confirm'),
    # url(r'^password-reset-complete$', 'authapp.views.password_reset_complete',  name='auth_password_reset_complete'),
)