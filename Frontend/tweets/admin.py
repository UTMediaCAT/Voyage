from django.contrib import admin
from tweets.models import Tweet, SourceSite, SourceTwitter, Keyword, CountLog
# Register your models here.

import os, yaml

class SourceSiteInline(admin.TabularInline):
    model = SourceSite
    fields = ['url', 'domain', 'matched']
    extra = 0

class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 0

class SourceTwitterInline(admin.TabularInline):
    model = SourceTwitter
    fields = ['name', 'matched']
    extra = 0

class CountLogInline(admin.TabularInline):
    model = CountLog
    fields = ['date', 'retweet_count', 'favorite_count']
    extra = 0

class TweetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['tweet_id', 'name', 'text']}),
        ('Date information', {'fields': ['date_added', 'date_published']})
        ]

    inlines = [SourceSiteInline, SourceTwitterInline, KeywordInline, CountLogInline]

    list_display = ('link_user', 'link_id', 'text', 'get_keywords', 'get_source_sites', 'get_source_twitters', 'date_published', 'date_added', 'link_options')

    search_fields = ['tweet_id', 'text', 'user', 'keyword__name', 'sourcesite__url', 'sourcetwitter__name']
    list_filter = ['name', 'keyword__name', 'sourcesite__name', 'sourcetwitter__name']
    ordering = ['-date_added']
    actions_on_top = True
    list_per_page = 100


    def get_keywords(self, obj):
        keywords = ''
        for key in obj.keyword_set.all():
            keywords += key.name + ', '
        return keywords[:-2]

    get_keywords.short_description = 'Matched Keywords'
    get_keywords.admin_order_field = 'keyword__name'

    def get_source_sites(self, obj):
        sources = ''
        for src in obj.sourcesite_set.all():
	    if src.matched:
                if 'http://www.' in src.url:
                    link = 'http://' + src.url[11:]
                else:
                    link = src.url
                sources += format('<a href="%s" target="_blank">%s</a>' % (link, link))
                sources += '<br>'
        return sources[:-4]

    get_source_sites.short_description = 'Matched Sources'
    get_source_sites.admin_order_field = 'sourcesite__url'
    get_source_sites.allow_tags = True

    def get_source_twitters(self, obj):
        accounts = ''
        for acc in obj.sourcetwitter_set.all():
            if acc.matched:
                accounts += acc.name + '<br>'
        return accounts[:-4]

    get_source_twitters.short_description = 'Matched Twitter Accounts'
    get_source_twitters.admin_order_field = 'sourcetwitter__name'
    get_source_twitters.allow_tags = True


    def link_id(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % ("https://twitter.com/" + obj.name + "/status/" + str(obj.tweet_id),
                                               obj.tweet_id))

    link_id.allow_tags = True
    link_id.admin_order_field = 'tweet_id'
    link_id.short_description = "Tweet ID"

    def link_user(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % ("https://twitter.com/" + obj.name,
                                               obj.name))

    link_user.allow_tags = True
    link_user.admin_order_field = 'name'
    link_user.short_description = "User"


    def link_options(self, obj):
        return format(('<a href="/admin/tweets/tweet/%s">Details</a><br>' +\
                       '<a href="/tweets/warc/%s">Download</a>') % (str(obj.pk), 'https:__twitter.com_' + obj.name + '_status_' + str(obj.tweet_id)))


    link_options.allow_tags = True
    link_options.short_description = "Options"

admin.site.register(Tweet, TweetAdmin)
