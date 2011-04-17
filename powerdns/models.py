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
    name       = models.CharField(verbose_name='Domain Name', max_length=255, db_index=True, help_text='eg: example.com')
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
        
    def generate_SOA(self, serial):
        """ 
        These are all server wide (not cluster wide) values and should be 
        stored somewhere acordingly.
        
        format: primary hostmaster serial refresh retry expire default_ttl 
        
        Discussed in rfc1912
        """
        primary = 'ns1.icedns.is'
        hostmaster = 'hostmaster.%s' % self.name
        serial  = serial
        refresh = '1200'    # 20 minutes
        retry   = '600'     # 10 minutes
        expire  = '4838400' # 8 weeks
        default_ttl = '172800' # 2 days
        return '%s %s %s %s %s %s %s'%(primary, hostmaster, serial, refresh, retry, expire, default_ttl)
        

    def save(self, *args, **kwargs):
        """ slug, and SOA record"""
        self.slug = slugify(self.name)
        self.notified_serial = int(time.time()) # epoch overflows 32bit unsigned int in 2106
        soa, created = Record.objects.get_or_create(domain=self, name=self.name, type='SOA')
        soa.content = self.generate_SOA(self.notified_serial)
        soa.save()
        
        super(Domain, self).save(*args, **kwargs)
    
    
class Record(models.Model):
    RECORD_TYPES = (
        ('A','A - IP v4 Address'),
        ('AAAA','AAAA - IP v6 Address'),
        ('CNAME','CNAME - Cononical name'),
        ('MX','MX - Mail exchanger'),
        ('SPF','SPF - Sender Permitted From'),
        ('SRV','SRV - Service location (encoded)'),
        ('TXT','TXT - Plain text data'),
        ('','----------'),
        ('AFSDB','AFSDB - AFS (RFC1183)'),
        ('CERT','CERT - (RFC2538)'),
        # ('DNSKEY','DNSKEY - DNSSEC record'),
        # ('DS','DS DNSSEC record'),
        ('HINFO','HINFO - eg: i386 Linux'),
        # ('KEY','KEY record (RFC2535)'),
        ('LOC','LOC - location (RFC2535)'),
        ('NAPTR','NAPTR - (RFC2915)'),
        ('NS','NS - Nameserver for a domain'),
        # ('NSEC','NSEC - DNSSEC record'),
        # ('PTR','PTR - Reverse pointer'), # We'll do reverse DNS separately
        ('RP','RP - Responsible Person'),
        # ('RRSIG','RRSIG DNSSEC record'),
        ('SSHFP','SSHFP - SSH fingerprint (RFC4255)'),

    )
    id         = models.AutoField(primary_key=True)
    domain     = models.ForeignKey('powerdns.Domain', null=True, blank=True, related_name='records',
                        db_column='domain_id', on_delete=models.CASCADE, db_index=True)
    name       = models.CharField(max_length=255, db_index=True, help_text='eg: www.example.com')
    type       = models.CharField(max_length=10, db_index=True, choices=RECORD_TYPES, default='')
    content    = models.CharField(max_length=255)
    ttl        = models.IntegerField(verbose_name='TTL', blank=True, null=True)
    prio       = models.IntegerField(verbose_name='Priority', blank=True, null=True, help_text='Only for MX records')
    change_date= models.IntegerField(blank=True, null=True)
    
    class Meta:
        db_table = 'records'

    def __unicode__(self):
        return '%s %s %s'%(self.type, self.name, self.content)
        
class Supermaster(models.Model):
    ip          = models.CharField(max_length=25, primary_key=True)
    nameserver  = models.CharField(max_length=255)
    owner       = models.ForeignKey('auth.User')

    class Meta:
        db_table = 'supermasters'
