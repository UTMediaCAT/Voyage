from django.contrib import admin
from articles.models import Article, Author, Source, Keyword
# Register your models here.

import yaml, os

class AuthorInline(admin.TabularInline):
    model = Author
    extra = 0

class SourceInline(admin.TabularInline):
    model = Source
    fields = ['url']
    extra = 0

class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 0
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['url', 'title']}),
        ('Date information', {'fields': ['date_added', 'date_published']})
        ]

    inlines = [AuthorInline, SourceInline, KeywordInline]

    list_display = ('link_url', 'title', 'get_authors', 'get_keywords', 'get_sources', 'date_published', 'date_added', 'link_warc')
    search_fields = ['url', 'title', 'author__author', 'keyword__keyword', 'source__url']
    list_filter = ['keyword__keyword', 'url_origin']
    ordering = ['-date_added']
    actions_on_top = True

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

    def get_authors(self, obj):
        authors = ''
        for ath in obj.author_set.all():
            authors += ath.author + ', '
        return authors[:-2]

    get_authors.short_description = 'Authors'
    get_authors.admin_order_field = 'author__author'

    def link_url(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url))

    link_url.allow_tags = True
    link_url.admin_order_field = 'url'
    link_url.short_description = "URL"

    def link_warc(self, obj):
        config_yaml = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../',"config.yaml")), 'r')
        config = yaml.load(config_yaml)['warc']
        config_yaml.close()

        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', config['dir']))
        return format('<a href="/articles/warc/%s">Download</a>' % (obj.url.replace('/', '\\')))


    link_warc.allow_tags = True
    link_warc.short_description = "Archived WARC"


admin.site.register(Article, ArticleAdmin)
