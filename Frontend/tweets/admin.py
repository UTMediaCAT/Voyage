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
        (None,               {'fields': ['tweet_id', 'user', 'text', 'followers']}),
        ('Date information', {'fields': ['date_added', 'date_published']})
        ]

    inlines = [SourceInline, KeywordInline]

    list_display = ('tweet_id', 'text', 'user', 'followers', 'get_keywords', 'get_sources', 'date_published', 'date_added')

    search_fields = ['tweet_id', 'text', 'user', 'followers', 'keyword__keyword', 'source__source']
    list_filter = ['keyword__keyword']
    ordering = ['-date_added']

    def get_keywords(self, obj):
        keywords = ''
        for key in obj.keyword_set.all():
            keywords += key.keyword + ', '
        return keywords[:-2]

    get_keywords.short_description = 'Matched Keywords'
    get_keywords.admin_order_field = 'keyword__keyword'

    def get_sources(self, obj):
        sources = ''
        for src in obj.source_set.all():
            sources += src.url + ', '
        return sources[:-2]

    get_sources.short_description = 'Matched Sources'
    get_sources.admin_order_field = 'source__source'

admin.site.register(Tweet, TweetAdmin)
