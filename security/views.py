"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login as django_login

from security.decorators import anonymous_required

@csrf_protect
@never_cache
@anonymous_required
def login(request, template_name='security/login.html',
          redirect_field_name=None,
          authentication_form=AuthenticationForm):
    
    response = django_login(request, template_name=template_name,
                            redirect_field_name=redirect_field_name)
    if request.method == 'POST':
        if response.status_code == 403:
            print "vobitten"
        else:
            print "granted"
    return response
    
 
    
def password_reset(request):
    return None