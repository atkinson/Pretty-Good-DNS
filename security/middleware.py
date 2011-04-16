"""
     ____  _      _          _   _   _     _                       
    |  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
    | |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
    |  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
    |_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

    Copyright 2011 (atkinsonr@gmail.com / @tkinson)
"""
from security.models import AuthenticatedSession
from django.contrib.sessions.models import Session

class DisallowMultipleSessionsMiddleware(object):
    def _get_remote_ip(self, request):
        """ What's the best way to get the clients IP address? """
        ip_addr = request.META.get('X-Real-IP')
        if not ip_addr:
            ip_addr = request.META.get('REMOTE_ADDR')
        return ip_addr
        
    def process_request(self, request):
        """ Gather details, record the session, expire the users previous session """
        try:
            session_key = request.session.session_key
        except:
            """ If there's no session then do nothing """
            return None
        """ If there's no user then do nothing """
        if request.user.is_anonymous():
            return None
            
        # Do we already have this session recorded?
        exists = AuthenticatedSession.objects.filter(user = request.user, session_key=session_key).exists()
        if not exists:
            # Then log this new session!
            login = AuthenticatedSession(user = request.user, 
                                         session_key=session_key,
                                         ip_address = self._get_remote_ip(request))
            login.save()
            # And delete any other sessions belonging to that user
            stale_sessions = AuthenticatedSession.objects.filter(user=request.user).exclude(session_key=session_key)
            for stale in stale_sessions:
                Session.objects.filter(pk=stale.session_key).delete()
