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

    list_display = ('title', 'url', 'get_authors', 'get_keywords', 'get_sources', 'date_published', 'date_added')
    search_fields = ['url', 'title', 'keyword__keyword', 'source__source']
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

    def get_authors(self, obj):
        authors = ''
        for ath in obj.author_set.all():
            authors += ath.author + ', '
        return authors[:-2]

    get_authors.short_description = 'Authors'
    get_authors.admin_order_field = 'author__author'

admin.site.register(Article, ArticleAdmin)
