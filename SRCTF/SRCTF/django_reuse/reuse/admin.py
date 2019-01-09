from django.contrib import admin
from .models import *
# Register your models here.
class GuestAdmin(admin.ModelAdmin):
    #def guest_pswd(self, instance):
    #    return instance.pswd_table.pswd
    model = Guest
    list_display = ['user','pswd','get_pswd','is_granted']
    search_fields = ['user__username']
    
    def get_pswd(self, obj):
        return obj.pswd.pswd

class PTAdmin(admin.ModelAdmin):
    list_display = ['id','pswd',]

class CtfInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'level']

class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['user', 'ctf', 'is_solved']
    search_fields = ['user__username', 'ctf__name', 'ctf__level']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ctype']
    
admin.site.register(Pswd_table, PTAdmin)    
admin.site.register(Guest, GuestAdmin)
admin.site.register(Ctf_info, CtfInfoAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Type)
admin.site.register(Tag)
admin.site.register(Cat_Tag)