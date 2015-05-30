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

    list_display = ('link_url', 'title', 'get_authors', 'get_keywords', 'get_sources', 'date_published', 'date_added', 'link_options')
    search_fields = ['url', 'title', 'author__name', 'keyword__name', 'source__url']
    list_filter = ['domain', 'keyword__name', 'source__domain']
    ordering = ['-date_added']
    actions_on_top = True

    def get_keywords(self, obj):
        keywords = ''
        for key in obj.keyword_set.all():
            keywords += key.name + ', '
        return keywords[:-2]

    get_keywords.short_description = 'Matched Keywords'
    get_keywords.admin_order_field = 'keyword__name'

    def get_sources(self, obj):
        sources = ''
        for src in obj.source_set.all():
            if 'http://www.' in src.url:
                link = 'http://' + src.url[11:]
            else:
                link = src.url
            sources += format('<a href="%s" target="_blank">%s</a>' % (link, link))
            sources += '<br>'
        return sources[:-4]

    get_sources.short_description = 'Matched Sources'
    get_sources.admin_order_field = 'source__url'
    get_sources.allow_tags = True

    def get_authors(self, obj):
        authors = ''
        for ath in obj.author_set.all():
            authors += ath.author + ', '
        return authors[:-2]

    get_authors.short_description = 'Authors'
    get_authors.admin_order_field = 'author__name'

    def link_url(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url))

    link_url.allow_tags = True
    link_url.admin_order_field = 'url'
    link_url.short_description = "URL"

    def link_options(self, obj):
        return format(('<a href="/admin/articles/article/%s">Details</a><br>' +\
                       '<a href="/articles/warc/%s">Download</a>') % (str(obj.pk), obj.url.replace('/', '_')))


    link_options.allow_tags = True
    link_options.short_description = "Options"


admin.site.register(Article, ArticleAdmin)
