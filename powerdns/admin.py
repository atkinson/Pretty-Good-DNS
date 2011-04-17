"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.contrib import admin
from powerdns.models import Domain, Record, Supermaster

class RecordInline(admin.TabularInline):
    model = Record
    exclude = ('change_date',)

class DomainAdmin(admin.ModelAdmin):
    exclude = ('type','master', 'last_check', 'notified_serial', 'slug')
    inlines = (
        RecordInline,
    )
admin.site.register(Domain, DomainAdmin)


class SupermasterAdmin(admin.ModelAdmin):
    pass
admin.site.register(Supermaster,SupermasterAdmin)
