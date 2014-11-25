from django.contrib import admin
from tweets.models import Tweet, Source, Keyword
# Register your models here.

import os, yaml

class SourceInline(admin.TabularInline):
    model = Source
    fields = ['url']
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

    list_display = ('link_user', 'link_id', 'text', 'get_keywords', 'get_sources', 'date_published', 'date_added', 'link_html')

    search_fields = ['tweet_id', 'text', 'user', 'keyword__keyword', 'source__url']
    list_filter = ['keyword__keyword', 'user']
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
    get_sources.admin_order_field = 'source__url'

    def link_id(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % ("https://twitter.com/" + obj.user + "/status/" + str(obj.tweet_id),
                                               obj.tweet_id))

    link_id.allow_tags = True
    link_id.admin_order_field = 'tweet_id'
    link_id.short_description = "Tweet ID"

    def link_user(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % ("https://twitter.com/" + obj.user,
                                               obj.user))

    link_user.allow_tags = True
    link_user.admin_order_field = 'user'
    link_user.short_description = "User"


    def link_html(self, obj):
        config_yaml = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../',"config.yaml")), 'r')
        config = yaml.load(config_yaml)['warc']
        config_yaml.close()

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', config['dir']))
        return format('<a href="/tweets/html/%s" >Download</a>' % 
                      ("https://twitter.com/" + obj.user + "/status/" + str(obj.tweet_id)).replace('/', '\\'))


    link_html.allow_tags = True
    link_html.short_description = "Archived HTML"

admin.site.register(Tweet, TweetAdmin)
