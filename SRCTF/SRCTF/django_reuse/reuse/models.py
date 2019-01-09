from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, default="TBD")
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name        
        
class Category(models.Model):
    name = models.CharField(max_length=100)
    typename = models.CharField(max_length=100)
    description = models.TextField(default="TBD")
    tags = models.ManyToManyField(Tag, through='Cat_Tag')
    ctype = models.ForeignKey(Type, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
        
class Cat_Tag(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.cat) + "||" + str(self.tag)
        
class Ctf_info(models.Model):
    name = models.CharField(max_length=100)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.IntegerField()
    status = models.CharField(max_length=10)
    author = models.CharField(max_length=50)
    src_path = models.CharField(max_length=200, default="not_a_dir")
    gen_path = models.CharField(max_length=200, default="not_a_gen")
    config_path = models.CharField(max_length=200, default="not_a_con")
    tags = models.ManyToManyField(Tag, through='Ctf_Tag')
    desc = models.TextField(default="TBD")
    
    def __str__(self):
        return self.name
    def __unicode__(self):
        return str(self.name)+'_'+str(self.level)
    class Meta:
        ordering = ['cat', 'level']

class Ctf_Tag(models.Model):
    ctf = models.ForeignKey(Ctf_info, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.ctf) + "||" + str(self.tag)

class Pswd_table(models.Model):
    pswd = models.CharField(max_length=20, default="123456")
    
    def __unicode__(self):
        return str(self.id)
        
class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_granted = models.BooleanField()
    u_dir = models.CharField(max_length=200)
    status = models.IntegerField(default="1")
    pswd = models.ForeignKey(Pswd_table, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default="0")   #used for scoreboard
    
    def __unicode__(self):
        return str(self.user)
        
    class Meta:
        ordering = ['user__username']

    
#class DoPswd(models.Model):
#    pswd = models.CharField(max_length=20, default="123456")
    
class Challenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ctf = models.ForeignKey(Ctf_info, on_delete=models.CASCADE)
    status = models.IntegerField()
    is_solved = models.BooleanField()
    flag = models.CharField(max_length=200)
    c_dir = models.CharField(max_length=200)
    #do_pswd = models.OneToOneField(DoPswd, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['user__username']
    

