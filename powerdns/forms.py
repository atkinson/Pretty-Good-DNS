"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django import forms
from powerdns.models import Domain, Record

class RecordForm(forms.ModelForm):
    """
    Used in by inlineformset_factory
    """
    class Meta:
        model = Record
        widgets = {
            'prio': forms.TextInput(attrs={'size': 3}),
            'ttl': forms.TextInput(attrs={'size': 3}),
        }



class DomainFormDummy(forms.ModelForm):
    """
    Used in by inlineformset_factory
    """
    class Meta:
        model = Domain
        exclude = ('slug', 'last_check', 'master', 'notified_serial', 'type', 'owner', 'name')
