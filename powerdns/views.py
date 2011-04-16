"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from powerdns.models import Domain, Record

def list_domains(request, template_name='powerdns/list_domains.html'):
    ctx = {
        'domain_list': Domain.objects.filter(owner=request.user)
    }
    return render_to_response(template_name, ctx, context_instance=RequestContext(request))

def domain_records(request, slug, template_name='powerdns/domain_records.html'):
    """ TODO Create a formset of records """
    ctx = {
        'domain': get_object_or_404(Domain, owner=request.user, slug=slug)
    }
    return render_to_response(template_name, ctx, context_instance=RequestContext(request))