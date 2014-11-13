from django.contrib import admin
from tweets.models import Tweet, Source, Keyword
# Register your models here.

class SourceInline(admin.TabularInline):
    model = Source
    extra = 0

class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 0

class TweetAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['tweet_id', 'user', 'followers']}),
		('Date information', {'fields': ['date_added', 'date_published']})
		]

	inlines = [SourceInline, KeywordInline]

	list_display = ('tweet_id', 'user', 'followers', 'date_published', 'date_added')

admin.site.register(Tweet, TweetAdmin)
