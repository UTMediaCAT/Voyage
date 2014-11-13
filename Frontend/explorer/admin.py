from django.contrib import admin
from explorer.models import Msite, Fsite, Keyword, Taccount
# Register your models here.


class MsiteAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['url', 'name', 'influence']})
		]


	list_display = ('name', 'url', 'influence')

class FsiteAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['url', 'name', 'influence']})
		]


	list_display = ('name', 'url', 'influence')

class KeywordAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['keyword']})
		]


	list_display = ['keyword']

class TaccountAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['account']})
		]


	list_display = ['account']

admin.site.register(Msite, MsiteAdmin)
admin.site.register(Fsite, FsiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Taccount, TaccountAdmin)