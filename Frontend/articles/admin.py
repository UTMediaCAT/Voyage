from django.contrib import admin
from articles.models import Article, Author, Source, Keyword
# Register your models here.

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

    list_display = ('title', 'link_url', 'get_authors', 'get_keywords', 'get_sources', 'date_published', 'date_added', 'link_warc')
    search_fields = ['url', 'title', 'author__author', 'keyword__keyword', 'source__url']
    list_filter = ['keyword__keyword', 'url_origin']
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

    def get_authors(self, obj):
        authors = ''
        for ath in obj.author_set.all():
            authors += ath.author + ', '
        return authors[:-2]

    get_authors.short_description = 'Authors'
    get_authors.admin_order_field = 'author__author'

    def link_url(self, obj):
        return format('<a href="%s">%s</a>' % (obj.url, obj.url))


    def link_warc(self, obj):
        return format('<a href="/articles/warc/%s" target="_blank">Download</a>' % (obj.url.replace('/', '\\')))


    link_url.allow_tags = True
    link_warc.allow_tags = True


admin.site.register(Article, ArticleAdmin)
