from django.contrib import admin
from explorer.models import Msite, Fsite, Keyword, Taccount
# Register your models here.


class MsiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]


    list_display = ('name', 'url')
    search_fields = ['name', 'url']
    ordering = ['name']

class FsiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]


    list_display = ('name', 'url')
    search_fields = ['name', 'url']
    ordering = ['name']

class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['keyword']})
        ]


    list_display = ['keyword']
    search_fields = ['keyword']

class TaccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['account']})
        ]


    list_display = ['account']
    search_fields = ['account']

admin.site.register(Msite, MsiteAdmin)
admin.site.register(Fsite, FsiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Taccount, TaccountAdmin)