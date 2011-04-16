/*
 ____  _      _          _   _   _     _                       
|  _ \(_) ___| |__      / \ | |_| | __(_)_ __  ___  ___  _ __  
| |_) | |/ __| '_ \    / _ \| __| |/ /| | '_ \/ __|/ _ \| '_ \ 
|  _ <| | (__| | | |  / ___ \ |_|   < | | | | \__ \ (_) | | | |
|_| \_\_|\___|_| |_| /_/   \_\__|_|\_\|_|_| |_|___/\___/|_| |_|

Copyright 2011 (atkinsonr@gmail.com / @tkinson)

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

(function() {
    jQuery.showMessage = function(message, options, callback){
        // defaults
        settings = jQuery.extend({
             id: 'sliding_message_box',
             position: 'bottom',
             size: '60',
             backgroundColor: 'rgb(45, 45, 45)',
             color: 'white',
             delay: 3000,
             speed: 500,
             fontSize: '26px'
        }, options);        
        
        var elem = $('#' + settings.id);
        var delayed;
        
        // generate message div if it doesn't exist
        if(elem.length == 0){
            elem = $('<div></div>').attr('id', settings.id);
            
            elem.css({'z-index': '999',
                      'background-color': settings.backgroundColor,
                      'color': settings.color,
                      'text-align': 'center',
                      'position': 'absolute',
                      'position': 'fixed',
                      'left': '0',
                      'width': '100%',
                      'line-height': settings.size + 'px',
                      'font-size': settings.fontSize
                      });
            
            $('body').append(elem);
        }
        
        elem.html(message);
        
        if(settings.position == 'bottom'){
            elem.css('bottom', '-' + settings.size + 'px');
            elem.animate({bottom:'0'}, settings.speed);
            delayed = function()
            {
                $("#"+settings.id).animate({bottom:"-"+settings.size+"px"}, settings.speed, callback);
            }
            setTimeout(delayed, settings.delay);
        }
        else if(settings.position == 'top'){
            elem.css('top', '-' + settings.size + 'px');
            elem.animate({top:'0'}, settings.speed);
            delayed = function()
            {
                $("#"+settings.id).animate({top:"-"+settings.size+"px"}, settings.speed, callback);
            }
            setTimeout(delayed, settings.delay);
        }
    }
})(jQuery);


(function() {
    jQuery.showMessages = function(messages, options)
    {
        if (messages && messages.length)
        {
            $.showMessage(messages.shift(), options, function()
            {
                $.showMessages(messages, options);
            });
        }
    }
})(jQuery);