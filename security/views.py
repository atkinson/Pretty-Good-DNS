"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from django.forms.util import ErrorList
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login as upstream_login

from security.decorators import anonymous_required
from security.models import FailedLoginAttempt
from security.forms import ReCaptchaForm, RaisedAuthenticationForm
from django.conf import settings

# Sensible defaults
LOGIN_RETRIES_TIMEOUT = getattr(settings, 'LOGIN_RETRIES_TIMEOUT', 60)
LOGIN_RETRIES_ALLOWED = getattr(settings, 'LOGIN_RETRIES_ALLOWED', 3)

def recaptcha_required(ip_address):
    """ Do we issue a ReCaptcha? """
    delta = datetime.timedelta(seconds = LOGIN_RETRIES_TIMEOUT)
    failed_attempts = FailedLoginAttempt.objects.filter(
                                ip_address = ip_address,
                                datetime__gt = datetime.datetime.now() - delta
                                ).count()
    return failed_attempts >= LOGIN_RETRIES_ALLOWED

@csrf_protect
@never_cache
@anonymous_required
def login(request, template_name='security/login.html',
          redirect_field_name=None,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """ 1. GET: Check which form to return, return form
        2. POST: Check which form we would have sent basedon IP
        3.  If we sent recaptcha, then check that. Fail if invalid.
        4.  Do upstream_login
        5.  Log if failed attempt """
    if request.method == 'POST':
        # Did we issue a recaptcha challenge? if so - check it!
        if recaptcha_required(request.META.get('REMOTE_ADDR')):
            form = RaisedAuthenticationForm(data=request.POST, ip_address=request.META.get('REMOTE_ADDR'))
            if not form.is_valid():
                form._errors["recaptcha"] = ErrorList()
                form._errors["username"] = ErrorList()
                form._errors["password"] = ErrorList()
                form._errors["recaptcha"].append("Please Try Again")
                return render_to_response(template_name, {'form': form },
                            context_instance=RequestContext(request, current_app=current_app))

        # ReCaptcha is all good so let Django authenticate
        response = upstream_login(request, template_name=template_name,
                                redirect_field_name=redirect_field_name)

        # What was the result of the authentication?
        login_unsuccessful = (
            response and
            not response.has_header('location') and
            response.status_code != 302
        )

        # Log a failed attempt
        if login_unsuccessful:
            try:
                user = User.objects.get(username=request.POST.get('username'))
            except:
                user = None
            fla = FailedLoginAttempt.objects.create(user = user,
                                     username = request.POST.get('username'),
                                     ip_address = request.META.get('REMOTE_ADDR'))
            fla.save()
            
    else: # GET
        if recaptcha_required(request.META.get('REMOTE_ADDR')):
            form = RaisedAuthenticationForm()
        else:
            form = AuthenticationForm()
        response = render_to_response(template_name, {'form': form },
                        context_instance=RequestContext(request, current_app=current_app))
    return response
    
 
    
def password_reset(request):
    return None
