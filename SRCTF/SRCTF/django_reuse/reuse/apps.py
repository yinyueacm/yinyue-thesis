from __future__ import unicode_literals

from django.apps import AppConfig
#from .models import Ctf_info

class ReuseConfig(AppConfig):
    name = 'reuse'
    def ready(self):
        print "Config ready!"
        from .models import Ctf_info
        import os
        web_list = Ctf_info.objects.filter(cat__ctype = 2)
        for webctf in web_list:
            ctfid = webctf.id
            container_name = "con_web_" + str(ctfid)
            os.popen('docker run -d -P -h SRCTF --name ' + container_name + ' mylamp')
        
        bin_list = Ctf_info.objects.filter(cat__ctype = 1)
        for binctf in bin_list:
            binid = binctf.id
            bindir = '/guests/bin_' + str(binid)
            os.popen('mkdir ' + bindir)
            container_name = "con_bin_" + str(binid)
            os.popen('docker run --privileged -d -P -h SRCTF --name ' + container_name + ' -v ' + str(bindir) + ':/src' + ' ctf14')
