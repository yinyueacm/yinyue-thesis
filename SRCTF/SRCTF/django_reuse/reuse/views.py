from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
import subprocess
import os
from django import forms
import utils
from .models import *
import random
import logging
from django.utils import timezone
# Create your views here.

logger = logging.getLogger('django')

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = "IP_NOT_FOUND"
    return ip
            

class SignupForm(forms.Form):
    def signup(self, request, user):
        root_dir = "/guests/guest_"
        user_dir = root_dir + str(user.id)
        os.popen('mkdir ' + user_dir)
        
        rand_pswd = random.randint(1, 99)
        guest = Guest(user_id = user.id, is_granted = 0, status = 0, u_dir = user_dir, pswd_id = rand_pswd)
        guest.save()

def index(request):
    template = loader.get_template('reuse/index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('reuse/about.html')
    #print utils.project_path
    context = {
    }
    # ip = get_ip(request)
    # log_msg = 'Someone get the about||'+ str(ip)
    # logger.info(log_msg)
    
    return HttpResponse(template.render(context, request))
    
def cat_view(request, catid):
    template = loader.get_template('reuse/cat_view.html')
    try:
        cat_info = Category.objects.get(pk = catid)
        uid = request.user.id
        guest = User.objects.get(pk = uid)
    except ObjectDoesNotExist:
        cat_info = None
        context = {
            'cat_info' : cat_info,
        }
        return HttpResponse(template.render(context, request))
    c_type = Type.objects.get(pk = cat_info.ctype_id)
    cat_tags = Cat_Tag.objects.filter(cat_id = catid)
    ret_cat_tags = Tag.objects.filter(pk__in=cat_tags)
    if (guest.guest.status == 2):#can view all challenges
        ctfs = Ctf_info.objects.filter(cat_id = catid).order_by('level')
    else:
        ctfs = Ctf_info.objects.filter(cat_id = catid, status = 1).order_by('level')
    
    context = {
        'cat_info' : cat_info,
        'c_type' : c_type,
        'ret_tags' : ret_cat_tags,
        'ctfs' : ctfs,
    }
    return HttpResponse(template.render(context, request))
    
def ctf_view(request, catid, ctfid):
    template = loader.get_template('reuse/ctf_view.html')
    #ctf = Ctf_info.objects.get(cat_id = catid, level = ctfid)
    try:
        ctf = Ctf_info.objects.get(cat_id = catid, level = ctfid)
        c_cat = Category.objects.get(pk = catid)
    except ObjectDoesNotExist:
        ctf = None
        c_cat = None
    port = None
    try:
        uid = request.user.id
        guest = User.objects.get(pk = uid)
        #print guest.id, ctf.id
        cha = Challenge.objects.get(user_id = guest.id, ctf_id = ctf.id)
    except:
        cha = None
        
    context = {
        'ctf' : ctf,
        'port' : port,
        'c_cat' : c_cat,
        'cha' : cha,
    }
    return HttpResponse(template.render(context, request))

def your_ctf(request):
    template = loader.get_template('reuse/work_on_ctf.html')
    ctf = None
    check_flag = None
    if ('ctfid' in request.GET):
        ctfid = request.GET['ctfid']
        uid = request.user.id
        dirname = "ctf_" + str(uid) + "_" + str(ctfid)
        
        try:
            ctf = Ctf_info.objects.get(pk = ctfid)
            guest = User.objects.get(pk = uid)
        except ObjectDoesNotExist:
            ctf = None
            port = None
            context = {
                'ctf' : ctf,
                'port' : port,
            }    
            return HttpResponse(template.render(context, request))
            
        ip = get_ip(request)
        now = timezone.localtime(timezone.now())
        log_msg = '[INFO '+ str(now) +'] User ' + str(guest.username) + '('+ str(guest.id) +') is trying to get ctf #' + str(ctf.id) + '||'+ str(ip)
        logger.info(log_msg)
            
        ctf_cat = Category.objects.get(pk = ctf.cat_id)
        # ctype=1 for binary exploitation
        if ((guest.guest.is_granted) and ((ctf.status == '1') or (guest.guest.status == 2)) and (guest.guest.u_dir is not None) and (ctf_cat.ctype_id == 1)):
            
            try:
                challenge = Challenge.objects.get(user_id = uid, ctf_id = ctfid)
            except ObjectDoesNotExist: #no challenge record
                c_flag = "FLAG_"
                confdir = str(ctf.config_path)
                if confdir != "not_a_con":
                    print confdir
                    conf = utils.getConf(utils.project_path + confdir)
                    fid = conf['flag_pre'] + str(utils.id_generator())
                    f = open(utils.project_path + conf['flag_dir'], 'w')
                    f.write(fid+'\n')
                    f.close()
                    c_flag = fid[fid.rfind('|')+1:]
            
                challenge = Challenge(user_id = uid, ctf_id = ctfid, status = 0, is_solved = 0, flag = c_flag, c_dir=dirname)
                challenge.save()
                
            container_name = "con_bin_" + str(ctfid)
            if ('flag' in request.GET):
                ctfflag = request.GET['flag']
                if ctfflag == challenge.flag:
                    check_flag = 1
                    #update the user information
                    if challenge.is_solved == 0:
                        challenge.is_solved = 1
                        #add 10 point for solving challenge to the guest 
                        guest_score = Guest.objects.get(user_id = uid)
                        guest_score.score += 10 
                        guest_score.save()
                        challenge.save()
                else:
                    check_flag = -1
                pswd = ""
            else:
                #no flag submisstion --> first time in this ctf
                #generate challenges and move to user dir
                '''confdir = str(ctf.config_path)
                if confdir is not "not_a_con":
                    conf = utils.getConf(confdir)
                    fid = conf['flag_pre'] + str(utils.id_generator())
                    f = open(conf['flag_dir'], 'w')
                    f.write(fid+'\n')
                    f.close()
                    challenge.flag = fid[fid.rfind('|')+1:]
                    challenge.save()'''
                dirname = "ctf_" + str(uid)
                guest_dir = '/guests/bin_'+ str(ctfid) + '/' + str(dirname)
                os.popen('mkdir ' + guest_dir)
                gen_path = utils.project_path + str(ctf.gen_path)
                os.popen(gen_path)
                src_path = utils.project_path + str(ctf.src_path)
                #os.popen('cp ' + src_path + '* ' + str(guest_dir) )
                os.popen('cp -r ' + src_path + '* ' + str(guest_dir) )
                #os.popen('docker run --privileged -d -P -h SRCTF --name ' + container_name + ' -v ' + str(guest_dir) + ':/home/guest/'+ dirname + ' ctf14')
                guest_name = "guest" + str(uid)
                guest_id = 7000 + int(uid)
                flag_name = "flag" + str(uid)
                flag_id = 9000 + int(uid)
                os.popen('docker exec -d '+ container_name + ' useradd -M -s /bin/bash -u ' + str(guest_id)+ ' ' + guest_name)
                os.popen('docker exec -d '+ container_name + ' useradd -M -s /sbin/nologin -u ' + str(flag_id)+ ' ' + flag_name)
                #pswd = utils.pswd_generator()
                pswd = Pswd_table.objects.get(pk = guest.guest.pswd_id).pswd
                
                #pswd_cmd = 'echo guest:'+str(pswd)+" | docker exec -i "+container_name + " chpasswd"
                pswd_cmd = 'echo ' + guest_name + ':'+str(pswd)+" | docker exec -i "+container_name + " chpasswd"
                os.popen(pswd_cmd)
                #privilege settings !!!Could be dangerous
                #filedir = "/home/ictf/cs@uga/ctfs/reuse_buffer_overflow/conf.json"
                confdir = str(ctf.config_path)
                if confdir != "not_a_con":
                    conf = utils.getConf(utils.project_path + confdir)
                    for cmd in conf['execs']:
                        #print cmd['cmd']
                        ft = ()
                        for i in range(0, cmd['num_args']):
                            earg = cmd['args'][i]
                            if earg == "__GUEST__":
                                earg = guest_name
                            elif earg == "__FLAG__":
                                earg = flag_name
                            elif earg == "__DIR__":
                                earg = dirname
                            ft = ft + ( earg, )
                        execline = 'docker exec ' + cmd['options']+ '-d ' + container_name + cmd['cmd'].format(ft)
                        #print execline
                        os.popen(execline)
            
            #To get the public port(in willa) binded for docker container
            proc1 = subprocess.Popen(['docker', 'port', container_name, '22'], stdout = subprocess.PIPE)
            portout = proc1.stdout.read()
            port = portout[portout.find(':')+1:]
            print port
            now = timezone.localtime(timezone.now())
            log_msg = '[INFO '+ str(now) +'] The docker #' + str(port).strip() + ' has been assigned to user ' + str(guest.username) + '('+ str(guest.id) +') for ctf #' + str(ctf.id) + '||'+ str(ip)
            logger.info(log_msg)
            '''
            #generate temp password image
            if pswd is not "":
                ic = utils.ImageChar()
                ic.draw_word(pswd)
                ic_name = str(uid) + "_" + str(ctfid)
                ic.save('/home/ictf/cs@uga/django_reuse/reuse/static/pswd/' + str(ic_name) + '.png') 
                #ic.save('static/pswd/' + str(ic_name) + '.png')'''
            cha = challenge
            
        # c_type=2 for web challenges
        elif ((guest.guest.is_granted) and ((ctf.status == '1') or (guest.guest.status == 2)) and (guest.guest.u_dir is not None) and (ctf_cat.ctype_id == 2)):
            try:
                challenge = Challenge.objects.get(user_id = uid, ctf_id = ctfid)
            except ObjectDoesNotExist: #no challenge record
                c_flag = "FLAG_"
                confdir = str(ctf.config_path)
                if confdir != "not_a_con":
                    print confdir
                    conf = utils.getConf(utils.project_path + confdir)
                    pre_flag = conf['flag_pre'] + str(utils.id_generator())
                    fid = pre_flag + conf['flag_post']
                    f = open(utils.project_path + conf['flag_dir'], 'w')
                    #print fid
                    f.write(fid+'\n')
                    f.close()
                    c_flag = pre_flag[pre_flag.find('FLAG_'):]
            
                challenge = Challenge(user_id = uid, ctf_id = ctfid, status = 0, is_solved = 0, flag = c_flag, c_dir=dirname)
                challenge.save()
            container_name = "con_web_" + str(ctfid)
            if ('flag' in request.GET):
                ctfflag = request.GET['flag']
                if ctfflag == challenge.flag:
                    check_flag = 1
                    #update the user information
                    if challenge.is_solved == 0:
                        challenge.is_solved = 1
                        #add 10 point for solving challenge to the guest 
                        guest_score = Guest.objects.get(user_id = uid)
                        guest_score.score += 10 
                        guest_score.save()
                        challenge.save()
                else:
                    check_flag = -1
                pswd = ""
            else:
                #no flag submisstion --> first time in this ctf
                #generate challenges and move to user dir
                guest_dir = guest.guest.u_dir + '/' + str(dirname)
                os.popen('mkdir ' + guest_dir)
                gen_path = utils.project_path + str(ctf.gen_path)
                #print gen_path
                os.popen(gen_path)
                src_path = utils.project_path + str(ctf.src_path)
                #os.popen('cp ' + src_path + '* ' + str(guest_dir) )
                os.popen('cp -r ' + src_path + '* ' + str(guest_dir) )
                os.popen('chmod -R 555 ' + str(guest_dir))
                os.popen('docker run -d -P -h SRCTF --name ' + container_name + ' mylamp')
                
                #os.popen('docker exec -d ' + container_name + ' mkdir /app/' + str(dirname))
                #print 'docker cp ' + str(guest_dir) + '/. ' + container_name + ':/app/' + str(dirname) + '/'
                os.popen('docker cp ' + str(guest_dir) + '/. ' + container_name + ':/app/' + str(dirname) + '/')
                
                #pswd = utils.pswd_generator()
                # pswd = Pswd_table.objects.get(pk = guest.guest.pswd_id).pswd
                
                # pswd_cmd = 'echo guest:'+str(pswd)+" | docker exec -i "+container_name + " chpasswd"
                # os.popen(pswd_cmd)
                #privilege settings !!!Could be dangerous
                #filedir = "/home/ictf/cs@uga/ctfs/reuse_buffer_overflow/conf.json"
                confdir = str(ctf.config_path)
                if confdir != "not_a_con":
                    conf = utils.getConf(utils.project_path + confdir)
                    for cmd in conf['execs']:
                        #print 'docker exec ' + cmd['options']+ '-d ' + container_name + cmd['cmd'] + dirname + cmd['extra']
                        os.popen('docker exec ' + cmd['options']+ '-d ' + container_name + cmd['cmd'] + dirname + cmd['extra'])
                    for sql in conf['sql']:
                        rstr = 'docker exec ' + '-i ' + container_name + sql['cmd']
                        #print rstr
                        #os.popen('/bin/bash -c \'{}\''.format(rstr))
                        subprocess.call(rstr, shell=True, executable="/bin/bash")
            
                    proc2 = subprocess.Popen(['docker', 'port', container_name, '3306'], stdout = subprocess.PIPE)
                    portout2 = proc2.stdout.read()
                    port2 = portout2[portout2.find(':')+1:].strip()
                    print port2
                    #portcmd = 'mysql -h127.0.0.1 -P'+ port2 + ' -uadmin -pyinyueacm sqlctf < ' + str(conf['sql_file'])
                    #print portcmd
                    #mysql -uadmin -pyinyueacm sqlctf < sqlctf.sql
                    # sqlcmd = 'docker exec -d '+ container_name +' /./import.sh'
                    # print sqlcmd
                    # os.popen(sqlcmd)
                    # os.popen(sqlcmd)
            
            #To get the public port(in willa) binded for docker container
            proc1 = subprocess.Popen(['docker', 'port', container_name, '80'], stdout = subprocess.PIPE)
            portout = proc1.stdout.read()
            port = portout[portout.find(':')+1:-1]
            print port
            now = timezone.localtime(timezone.now())
            log_msg = '[INFO '+ str(now) +'] The docker #' + str(port).strip() + ' has been assigned to user ' + str(guest.username) + '('+ str(guest.id) +') for ctf #' + str(ctf.id) + '||'+ str(ip)
            logger.info(log_msg)
            cha = challenge
        # c_type=3 for reverse challenges
        elif ((guest.guest.is_granted) and ((ctf.status == '1') or (guest.guest.status == 2)) and (guest.guest.u_dir is not None) and (ctf_cat.ctype_id == 3)):
            try:
                challenge = Challenge.objects.get(user_id = uid, ctf_id = ctfid)
            except ObjectDoesNotExist: #no challenge record
                c_flag = "FLAG_"
                confdir = str(ctf.config_path)
                if confdir != "not_a_con":
                    print confdir
                    conf = utils.getConf(utils.project_path + confdir)
                    c_flag = conf['flag']
                challenge = Challenge(user_id = uid, ctf_id = ctfid, status = 0, is_solved = 0, flag = c_flag, c_dir=dirname)
                challenge.save()
            if ('flag' in request.GET):
                ctfflag = request.GET['flag']
                if ctfflag == challenge.flag:
                    check_flag = 1
                    #update the user information
                    if challenge.is_solved == 0:
                        challenge.is_solved = 1
                        #add 10 point for solving challenge to the guest 
                        guest_score = Guest.objects.get(user_id = uid)
                        guest_score.score += 10 
                        guest_score.save()
                        challenge.save()
                else:
                    check_flag = -1
                pswd = ""
            else:
                #no flag submisstion --> first time in this ctf
                print "Solving reverse challenges!"
                
            now = timezone.localtime(timezone.now())
            log_msg = '[INFO '+ str(now) +'] User ' + str(guest.username) + '('+ str(guest.id) +') is solving reverse(static) ctf #' + str(ctf.id) + '||'+ str(ip)
            logger.info(log_msg)
            cha = challenge
            port = 99999
        # do not provide challenge because of the config settings        
        else:
            port = -1
            cha = None
    else:
        port = None
        cha = None
        
    context = {
        'ctf' : ctf,
        'port' : port,
        'cha' : cha,
        'check_flag' : check_flag
    }    
    return HttpResponse(template.render(context, request))
        
def your_flag(request):
    template = loader.get_template('reuse/work_on_ctf.html')
        
'''def start_ctf(request):
    if(request.GET.get('start_ctf')):
        subprocess.call(['/home/ictf/cs@uga/start_ctf.sh'])
    context = {
        'port' : 1,
    }
    
    return render(context, 'reuse/ctf_view.html')'''

def scoreboard(request):
    score_list = Guest.objects.filter(status = 1).order_by('-score','user__username')
    return render(request,"reuse/scoreboard.html",{'score_list':score_list})    
        
        
    
