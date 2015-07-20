from django.contrib import admin
from explorer.models import ReferringSite, SourceSite, Keyword, ReferringTwitter, SourceTwitter
from articles.models import Article
from articles.models import SourceSite as ArticleSource
from articles.models import Keyword as ArticleKeyword
from tweets.models import Tweet
from tweets.models import SourceSite as TwitterSource
from tweets.models import Keyword as TwitterKeyword
from django.utils import timezone

class ReferringSiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name', 'mode']})
        ]
    list_display = ('name', 'url', 'article_count', 'latest_article', 'mode')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True
    list_per_page = 1000

    def article_count(self, obj):
        return len(Article.objects.filter(domain=obj.url))

    article_count.short_description = "Total Articles Archived"

    def latest_article(self, obj):
        latest = Article.objects.filter(domain=obj.url)
        if latest:
            delta = timezone.now() - latest.latest('date_added').date_added
            t1 = delta.days             # Days
            t2 = delta.seconds/3600     # Hours
            t3 = delta.seconds%3600/60  # Minutes
            return ('%2d days %2d hours %2d min ago' % (t1, t2, t3))
        else:
            return 'Have not found any articles yet!'
    latest_article.short_description = 'Last Found'


class SourceSiteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]
    list_display = ('name', 'url', 'cited_count')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True
    list_per_page = 1000

    def cited_count(self, obj):
        return len(ArticleSource.objects.filter(domain=obj.url)) + \
               len(TwitterSource.objects.filter(domain=obj.url))

    cited_count.short_description = "Total Cites"


class KeywordAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']})
        ]


    list_display = ['name', 'match_count']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def match_count(self, obj):
        return len(ArticleKeyword.objects.filter(name=obj.name)) + \
               len(TwitterKeyword.objects.filter(name=obj.name))

    match_count.short_description = "Total Matches"

class ReferringTwitterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']})
        ]


    list_display = ['name', 'tweet_count', 'latest_tweet']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def tweet_count(self, obj):
        return len(Tweet.objects.filter(name__iexact=obj.name))

    tweet_count.short_description = "Total Tweets Archived"


    def latest_tweet(self, obj):
        latest = Tweet.objects.filter(name__iexact=obj.name)
        if latest:
            delta = timezone.now() - latest.latest('date_added').date_added
            t1 = delta.days             # Days
            t2 = delta.seconds/3600     # Hours
            t3 = delta.seconds%3600/60  # Minutes
            return '%-2d days %-2d hours %-2d min ago' % (t1, t2, t3)
        else:
            return 'Have not found any tweets yet!'

    latest_tweet.short_description = 'Last Found'

class SourceTwitterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']})
        ]


    list_display = ['name']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

admin.site.register(ReferringSite, ReferringSiteAdmin)
admin.site.register(SourceSite, SourceSiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(ReferringTwitter, ReferringTwitterAdmin)
admin.site.register(SourceTwitter, SourceTwitterAdmin)
