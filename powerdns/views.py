"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.db import transaction
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms.models import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from powerdns.models import Domain, Record
from powerdns.forms import DomainFormDummy, RecordForm

@login_required
def list_domains(request, template_name='powerdns/list_domains.html'):
    """ List all domains for current user """
    ctx = {
        'domain_list': Domain.objects.filter(owner=request.user)
    }
    return render_to_response(template_name, ctx, context_instance=RequestContext(request))

@login_required
@transaction.commit_on_success
def domain_records(request, slug, template_name='powerdns/domain_records.html',
                   post_redirect='powerdns.views.domain_records', cancel='powerdns.views.list_domains'):
    """ Edit a domain and records if it is owned by the current user """
    domain = get_object_or_404(Domain, owner=request.user, slug=slug)
    ctx = {
       'cancel': reverse(cancel),
       'domain': domain
    }

    RecordsInlineFormset = inlineformset_factory(Domain, Record, extra=1, form=RecordForm)

    if request.method == "POST":
        form = DomainFormDummy(data=request.POST, instance=domain)
        records_formset = RecordsInlineFormset(request.POST, instance=domain, prefix='records')
        if form.is_valid() and records_formset.is_valid():
            records_formset.save()
            form.save()
            messages.add_message(request, messages.INFO, 'Changes to %s have been saved!'% domain)
            return HttpResponseRedirect(reverse(post_redirect, kwargs={'slug':slug}))
    else:
        form = DomainFormDummy(instance=domain)
        records_formset = RecordsInlineFormset(instance=domain, prefix='records', queryset=Record.objects.exclude(type__iexact='SOA'))
    ctx.update({
        'records_formset': records_formset,
        'form': form
    })
    return render_to_response(template_name, ctx, context_instance=RequestContext(request))