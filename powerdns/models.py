"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
import time
from django.db import models
from django.template.defaultfilters import slugify

class Domain(models.Model):
    id         = models.AutoField(primary_key=True)
    name       = models.CharField(max_length=255, db_index=True)
    slug       = models.SlugField()
    master     = models.CharField(max_length=128, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type       = models.CharField(max_length=6, default='MASTER')
    notified_serial = models.IntegerField(blank=True, null=True)
    owner      = models.ForeignKey('auth.User')
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        db_table = 'domains'
        
    def generate_SOA(self):
        """ primary hostmaster serial refresh retry expire default_ttl """
        primary = 'ns1.icedns.is'
        hostmaster = 'hostmaster.%s' % self.name
        serial  = int(time.time())
        refresh = '3600'
        retry   = '600'
        expire  = '604800'
        default_ttl = '1800'
        return '%s %s %s %s %s %s %s'%(primary, hostmaster, serial, refresh, retry, expire, default_ttl)
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        soa, created = Record.objects.get_or_create(domain=self, name=self.name, type='SOA')
        soa.content = self.generate_SOA()
        soa.save()
        super(Domain, self).save(*args, **kwargs)
    
    
class Record(models.Model):
    RECORD_TYPES = (
        ('A','A - IPv4 Address'),
        ('AAAA','AAAA - IPv6 Address'),
        ('AFSDB','AFSDB - for Andrew File System (AFS)'),
        ('CERT','CERT - Certificate (RFC 2538)'),
        ('CNAME','CNAME - Cononical name'),
        # ('DNSKEY','DNSKEY - DNSSEC record'),
        # ('DS','DS DNSSEC record'),
        ('HINFO','HINFO - Hardware info eg: i386 linux'),
        # ('KEY','KEY record (RFC 2535)'),
        ('LOC','LOC - location record (RFC 2535)'),
        ('MX','MX - Mail exchanger'),
        ('NAPTR','NAPTR - Naming Authority Pointer (RFC 2915)'),
        ('NS','NS - Nameserver for a domain'),
        # ('NSEC','NSEC - DNSSEC record'),
        ('PTR','PTR - Reverse pointer'),
        ('RP','RP - Responsible Person'),
        # ('RRSIG','RRSIG DNSSEC record'),
        # ('SOA','SOA - Start of Authority'),
        ('SPF','SPF - Sender Permitted From'),
        ('SSHFP','SSHFP - SSH fingerprints (RFC 4255'),
        ('SRV','SRV - Encoded port and location of a service'),
        ('TXT','TXT - Plain text data'),
    )
    id         = models.AutoField(primary_key=True)
    domain     = models.ForeignKey('powerdns.Domain', null=True, blank=True, related_name='records',
                        db_column='domain_id', on_delete=models.CASCADE, db_index=True)
    name       = models.CharField(max_length=255, db_index=True)
    type       = models.CharField(max_length=10, db_index=True, choices=RECORD_TYPES)
    content    = models.CharField(max_length=255)
    ttl        = models.IntegerField(verbose_name='TTL', blank=True, null=True)
    prio       = models.IntegerField(verbose_name='Priority', blank=True, null=True, help_text='Only for MX records')
    change_date= models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'records'

    def __unicode__(self):
        return '%s %s %s'%(self.name, self.type, self.content)
        
class Supermaster(models.Model):
    ip          = models.CharField(max_length=25, primary_key=True)
    nameserver  = models.CharField(max_length=255)
    owner       = models.ForeignKey('auth.User')

    class Meta:
        db_table = 'supermasters'
