"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.db import models


class Domain(models.Model):
    id         = models.AutoField(primary_key=True)
    name       = models.CharField(max_length=255, db_index=True)
    master     = models.CharField(max_length=128, null=True)
    last_check = models.IntegerField(null=True)
    type       = models.CharField(max_length=6)
    notified_serial = models.IntegerField(null=True)
    account    = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'domains'
    
    
class Record(models.Model):
    id         = models.AutoField(primary_key=True)
    domain     = models.ForeignKey('powerdns.Domain', null=True, db_column='domain_id',
                                                      on_delete=models.CASCADE, db_index=True)
    name       = models.CharField(max_length=255, db_index=True)
    type       = models.CharField(max_length=10, db_index=True)
    content    = models.CharField(max_length=255)
    ttl        = models.IntegerField(null=True)
    prio       = models.IntegerField(null=True)
    change_date= models.IntegerField(null=True)
    
    class Meta:
        db_table = 'records'


class Supermaster(models.Model):
    ip          = models.CharField(max_length=25, primary_key=True)
    nameserver  = models.CharField(max_length=255)
    account     = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'supermasters'
