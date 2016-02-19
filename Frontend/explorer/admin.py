from django.contrib import admin
from django.contrib.contenttypes.admin import (GenericStackedInline, GenericTabularInline)
from taggit.models import TaggedItem
from explorer.models import ReferringSite, ReferringSiteFilter, ReferringSiteCssSelector, SourceSite, Keyword, KeywordAlias, ReferringTwitter, SourceTwitter
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


class ReferringSiteAdminForm(forms.ModelForm):
    class Meta:
        Model = ReferringSite

    def clean(self):
        url = self.cleaned_data['url']
        check = self.cleaned_data['check']

        if check:
            count = newspaper.build(url, memoize_articles=False,
                            keep_article_html=False,
                            fetch_images=False,
                            language='en').size()
            raise forms.ValidationError(mark_safe(('Newspaper RSS scan found %i articles.<br>' +
                                                   'If this amount doesn\'t seem right, consider changing scanner to <i>MediaCAT Crawler</i> or <i>Both</i>.<br>' +
                                                   'Uncheck \'Test Newspaper RSS Scan\' after you choose the scanner to dismiss this message.')%count))
            #self.add_error('check', 'Newspaper found %i articles.'%count)
        return self.cleaned_data


class ReferringSiteAdmin(admin.ModelAdmin):
    model = ReferringSite
    form = ReferringSiteAdminForm
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['url', 'name', 'mode', 'check']})
        ]
    inlines += [ReferringSiteFilterInline, ReferringSiteCssSelectorInline]
    list_display = ('name', 'url', 'article_count', 'latest_article', 'mode', 'get_tags')
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

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class SourceSiteAdmin(admin.ModelAdmin):
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['url', 'name']})
        ]
    list_display = ('name', 'url', 'cited_count', 'get_tags')
    search_fields = ['name', 'url']
    ordering = ['name']
    actions_on_top = True
    list_per_page = 1000

    def cited_count(self, obj):
        return len(ArticleSource.objects.filter(domain=obj.url)) + \
               len(TwitterSource.objects.filter(domain=obj.url))

    cited_count.short_description = "Total Cites"

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class KeywordAliasInline(admin.TabularInline):
    model = KeywordAlias
    extra = 1


class KeywordAdmin(admin.ModelAdmin):
    inlines = [KeywordAliasInline, TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name']})
        ]


    list_display = ['name', 'match_count', 'get_aliases', 'get_tags']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def match_count(self, obj):
        return len(ArticleKeyword.objects.filter(name=obj.name)) + \
               len(TwitterKeyword.objects.filter(name=obj.name))

    match_count.short_description = "Total Matches"

    def get_aliases(self, obj):
        aliases = []
        for alias in obj.keywordalias_set.all():
            aliases.append(str(alias.name))
        return ', '.join(aliases)

    get_aliases.short_description = "Aliases"

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class ReferringTwitterAdmin(admin.ModelAdmin):
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name']})
        ]

    list_display = ['name', 'tweet_count', 'latest_tweet', 'get_tags']
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

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


class SourceTwitterAdmin(admin.ModelAdmin):
    inlines = [TaggitTabularInline]
    list_filter = [TaggitListFilter]
    fieldsets = [
        (None,               {'fields': ['name']})
        ]

    list_display = ['name', 'get_tags']
    search_fields = ['name']
    actions_on_top = True
    list_per_page = 1000

    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tags.append(str(tag))
        return ', '.join(tags)

    get_tags.short_description = "Tags"


admin.site.register(ReferringSite, ReferringSiteAdmin)
admin.site.register(SourceSite, SourceSiteAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(ReferringTwitter, ReferringTwitterAdmin)
admin.site.register(SourceTwitter, SourceTwitterAdmin)
