"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from django.db import models

class AuthenticatedSession(models.Model):
    """  Record of an authenticated session  """
    user = models.ForeignKey('auth.User', related_name='authenticated_sessions')
    datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.IPAddressField(null=True)
    session_key = models.CharField(max_length=40)
