from django.contrib import admin
from explorer.models import Msite, Fsite, Keyword, Taccount
from articles.models import Article
from articles.models import Source as ASource
from articles.models import Keyword as AKeyword
from tweets.models import Tweet
from tweets.models import Source as TSource
from tweets.models import Keyword as TKeyword

from django.utils import timezone

class MsiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]
    list_display = ('name', 'url', 'article_count', 'latest_article')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True


    def article_count(self, obj):
        return len(Article.objects.filter(url_origin=obj.url))

    article_count.short_description = "Total Articles Archived"


    def latest_article(self, obj):
        latest = Article.objects.filter(url_origin=obj.url)
        if latest:
            delta = timezone.now() - latest.latest('date_added').date_added
            t1 = delta.days             # Days
            t2 = delta.seconds/3600     # Hours
            t3 = delta.seconds%3600/60  # Minutes
            return '%-2d days %-2d hours %-2d min ago' % (t1, t2, t3)
        else:
            return 'Have not found any articles yet!'

    latest_article.short_description = 'Last Found'


class FsiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]
    list_display = ('name', 'url', 'cited_count')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True

    def cited_count(self, obj):
        return len(ASource.objects.filter(url_origin=obj.url)) + \
               len(TSource.objects.filter(url_origin=obj.url))

    cited_count.short_description = "Total Cites"


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['keyword']})
        ]


    list_display = ['keyword', 'match_count']
    search_fields = ['keyword']
    actions_on_top = True

    def match_count(self, obj):
        return len(AKeyword.objects.filter(keyword=obj.keyword)) + \
               len(TKeyword.objects.filter(keyword=obj.keyword))

    match_count.short_description = "Total Matches"

class TaccountAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['account']})
        ]


    list_display = ['account', 'tweet_count', 'latest_tweet']
    search_fields = ['account']
    actions_on_top = True

    def tweet_count(self, obj):
        return len(Tweet.objects.filter(user=obj.account))

    tweet_count.short_description = "Total Tweets Archived"


    def latest_tweet(self, obj):
        latest = Tweet.objects.filter(user=obj.account)
        if latest:
            delta = timezone.now() - latest.latest('date_added').date_added
            t1 = delta.days             # Days
            t2 = delta.seconds/3600     # Hours
            t3 = delta.seconds%3600/60  # Minutes
            return '%-2d days %-2d hours %-2d min ago' % (t1, t2, t3)
        else:
            return 'Have not found any tweets yet!'

    latest_tweet.short_description = 'Last Found'


admin.site.register(Msite, MsiteAdmin)
admin.site.register(Fsite, FsiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Taccount, TaccountAdmin)