from django.contrib import admin
from django.contrib.contenttypes.admin import (GenericStackedInline, GenericTabularInline)
from taggit.models import TaggedItem
from explorer.models import ReferringSite, ReferringSiteFilter, ReferringSiteCssSelector, SourceSite, SourceSiteAlias, Keyword, ReferringTwitter, SourceTwitter, SourceTwitterAlias, ReferringTwitterIgnoreURL, ReferringTwitterHashtag, ReferringTwitterMention
from articles.models import Article
from articles.models import SourceSite as ArticleSource
from articles.models import Keyword as ArticleKeyword
from tweets.models import Tweet
from tweets.models import SourceSite as TwitterSource
from tweets.models import Keyword as TwitterKeyword
from django.utils import timezone
from django import forms
import newspaper
from django.utils.safestring import mark_safe
from django.forms import BaseInlineFormSet

# For url encoding of shortcut links
import urllib.request, urllib.parse, urllib.error

class TaggitListFilter(admin.SimpleListFilter):
    """
    Filter records by Taggit tags for the current model only.
    Tags are sorted alphabetically by name.
    """

    title = 'Tags'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        model_tags = [tag.name for tag in
            TaggedItem.tags_for(model_admin.model)]
        model_tags.sort()
        return tuple([(tag, tag) for tag in model_tags])

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(tags__name=self.value())


class TaggitInlineBase():
    """
    Base model for Taggit admin inlines.
    Use TaggitStackedInline or TaggitTabularInline.
    """
    model = TaggedItem
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'
    ordering = ('tag__name',)
    extra = 1


class TaggitTabularInline(TaggitInlineBase, GenericTabularInline):
    """
    Add tabular inline for Taggit tags to admin.
    Tags are sorted alphabetically by name.
    """
    pass


class ReferringSiteFilterInline(admin.TabularInline):
    model = ReferringSiteFilter
    extra = 0


class ReferringSiteCssSelectorInline(admin.TabularInline):
    model = ReferringSiteCssSelector
    extra = 0


# class ReferringSiteAdminForm(forms.ModelForm):
#     class Meta:
#         Model = ReferringSite

#     def clean(self):
#         url = self.cleaned_data['url']
#         check = self.cleaned_data['check']

#         if check:
#             count = newspaper.build(url, memoize_articles=False,
#                             keep_article_html=False,
#                             fetch_images=False,
#                             language='en').size()
#             raise forms.ValidationError(mark_safe(('Newspaper RSS scan found %i articles.<br>' +
#                                                    'If this amount doesn\'t seem right, consider changing scanner to <i>MediaCAT Crawler</i> or <i>Both</i>.<br>' +
#                                                    'Uncheck \'Test Newspaper RSS Scan\' after you choose the scanner to dismiss this message.')%count))
#             #self.add_error('check', 'Newspaper found %i articles.'%count)
#         return self.cleaned_data


class ReferringSiteAdmin(admin.ModelAdmin):
    model = ReferringSite
    # form = ReferringSiteAdminForm
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['url', 'name', 'mode']})
        ]
    inlines += [ReferringSiteFilterInline, ReferringSiteCssSelectorInline]
    list_display = ('name', 'url', 'article_count', 'latest_article', 'mode', 'is_shallow', 'get_tags')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True
    list_per_page = 1000

    change_form_template = 'admin/referringSite_change_form.html'

    def article_count(self, obj):
        url = obj.url
        return '<a target="_blank" href="/admin/articles/article/?q=&domain=' + \
            str(urllib.parse.quote_plus(url)) + '">' + \
            str(Article.objects.filter(domain=obj.url).count()) +\
            '</a>'

    article_count.short_description = "Total Articles Archived"
    article_count.allow_tags = True

    def latest_article(self, obj):
        latest = Article.objects.filter(domain=obj.url).last()
        if latest:
            latest = latest.version_set
            tznow = timezone.now()
            latestadded = latest.latest('date_added').date_added
            # temporary fix ---
            if (latestadded == None):
                return 'Last date_added not found...'
            delta = tznow - latestadded
            t1 = delta.days             # Days
            t2 = delta.seconds/3600     # Hours
            t3 = delta.seconds%3600/60  # Minutes
            return ('%2d days %2d hours %2d min ago' % (t1, t2, t3))
            # return latest.latest('date_added')
        else:
            return 'Have not found any articles yet!'
    latest_article.short_description = 'Last Found'

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class SourceSiteAliasInline(admin.TabularInline):
    model = SourceSiteAlias
    extra = 1


class SourceSiteAdmin(admin.ModelAdmin):
    inlines = [SourceSiteAliasInline, TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]
    list_display = ('name', 'url', 'total_cites_count', 'get_aliases', 'get_tags')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True
    list_per_page = 1000

    def total_cites_count(self, obj):
        # Domain is stored without last forward slash
        url = obj.url[:-1] if obj.url[-1] == '/' else obj.url
        article_cites_count = Article.objects.filter(version__sourcesite__domain=url).distinct().count()
        article_tag = '<a target="_blank" href="/admin/articles/sourcedarticle/?q=&version__sourcesite__domain=' + \
            str(urllib.parse.quote_plus(url)) + '">' + \
            str(article_cites_count) + \
            '</a>'
        tweet_cites_count = Tweet.objects.filter(sourcesite__domain=url).distinct().count()
        tweet_tag = '<a target="_blank" href="/admin/tweets/tweet/?q=&sourcesite__domain=' + \
            str(urllib.parse.quote_plus(url)) + '">' + \
            str(tweet_cites_count) + \
            '</a>'
        total_cites_count = article_cites_count + tweet_cites_count
        return '<span>{} ({} / {})</span>'.format(total_cites_count, article_tag, tweet_tag)

    total_cites_count.short_description = "Total Cites (Articles/Tweets)"
    total_cites_count.allow_tags = True

    def get_aliases(self, obj):
        aliases = []
        for alias in obj.sourcesitealias_set.all():
            aliases.append(str(alias))
        return ', '.join(aliases)

    get_aliases.short_description = "Aliases"

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class KeywordAdmin(admin.ModelAdmin):
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name']})
        ]


    list_display = ['name', 'total_match_count', 'get_tags']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def total_match_count(self, obj):
        article_match_count = Article.objects.filter(version__keyword__name=obj.name).distinct().count()
        article_tag = '<a target="_blank" href="/admin/articles/article/?q=&version__keyword__name=' + \
            str(urllib.parse.quote_plus(obj.name)) + '">' + \
            str(article_match_count) + \
            '</a>'
        tweet_match_count = Tweet.objects.filter(keyword__name=obj.name).distinct().count()
        tweet_tag = '<a target="_blank" href="/admin/tweets/tweet/?q=&keyword__name=' + \
            str(urllib.parse.quote_plus(obj.name)) + '">' + \
            str(tweet_match_count) + \
            '</a>'
        total_match_count = article_match_count + tweet_match_count
        return '<span>{} ({} / {})</span>'.format(total_match_count, article_tag, tweet_tag)

    total_match_count.short_description = "Total Matches (Articles/Tweets)"
    total_match_count.allow_tags = True

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class ReferringTwitterIgnoreURLInline(admin.TabularInline):
    model = ReferringTwitterIgnoreURL
    extra = 0


class ReferringTwitterAdmin(admin.ModelAdmin):
    inlines = [TaggitTabularInline, ReferringTwitterIgnoreURLInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name', 'top_hashtag', 'top_mention']})
        ]
    readonly_fields = ('top_hashtag', 'top_mention')

    list_display = ['name', 'tweet_count', 'tweet_visited', 'latest_tweet', 'get_tags']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def top_mention(self, obj):
        result = "<table> <tr> <th> </th> <th> </th> </tr>"
        for q in ReferringTwitterMention.objects.filter(user=obj).order_by("-count", "screen_name")[:30]:
            result += "<tr> <td> " + str(q) + "</td> <td>" + str(q.count) + "</td> </tr>" 
        return result + "</table>"

    def top_hashtag(self, obj):
        result = "<table> <tr> <th> </th> <th> </th> </tr>"
        for q in ReferringTwitterHashtag.objects.filter(user=obj).order_by("-count", "text")[:30]:
            result += "<tr> <td> {} </td> <td> {} </td> </tr>".format(str(q), str(q.count)) 
        return result + "</table>"

    top_mention.short_description = "Top Mentions"
    top_hashtag.short_description = "Top Hashtags"

    def tweet_count(self, obj):
        return '<a target="_blank" href="/admin/tweets/tweet/?q=&name=' + \
            str(urllib.parse.quote_plus(obj.name)) + '">' + \
            str(Tweet.objects.filter(name__iexact=obj.name).count()) +\
            '</a>'
    tweet_count.short_description = "Total Tweets Archived"
    tweet_count.allow_tags = True

    def tweet_visited(self, obj):
        return obj.tweets_visited + obj.timeline_tweets
    tweet_visited.short_description = "Total Tweets Visited"

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

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class SourceTwitterAliasInline(admin.TabularInline):
    model = SourceTwitterAlias
    extra = 1


class SourceTwitterAdmin(admin.ModelAdmin):
    inlines = [SourceTwitterAliasInline, TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name']})
        ]

    list_display = ['name', 'total_mention_count', 'get_aliases', 'get_tags']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def total_mention_count(self, obj):
        article_match_count = Article.objects.filter(version__sourcetwitter__name=obj.name).distinct().count()
        article_tag = '<a target="_blank" href="/admin/articles/article/?q=&version__sourcetwitter__name=' + \
            str(urllib.parse.quote_plus(obj.name)) + '">' + \
            str(article_match_count) + \
            '</a>'
        tweet_match_count = Tweet.objects.filter(sourcetwitter__name=obj.name).distinct().count()
        tweet_tag = '<a target="_blank" href="/admin/tweets/tweet/?q=&sourcetwitter__name=' + \
            str(urllib.parse.quote_plus(obj.name)) + '">' + \
            str(tweet_match_count) + \
            '</a>'
        total_match_count = article_match_count + tweet_match_count
        return '<span>{} ({} / {})</span>'.format(total_match_count, article_tag, tweet_tag)

    total_mention_count.short_description = "Total Mentions (Articles/Tweets)"
    total_mention_count.allow_tags = True

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    def get_aliases(self, obj):
        aliases = []
        for alias in obj.sourcetwitteralias_set.all():
            aliases.append(str(alias))
        return ', '.join(aliases)

    get_aliases.short_description = "Aliases"

    get_tags.short_description = "Tags"


admin.site.register(ReferringSite, ReferringSiteAdmin)
admin.site.register(SourceSite, SourceSiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(ReferringTwitter, ReferringTwitterAdmin)
admin.site.register(SourceTwitter, SourceTwitterAdmin)
