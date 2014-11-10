from django.contrib import admin
from articles.models import Article, Author, Source, Keyword
# Register your models here.

class AuthorInline(admin.TabularInline):
    model = Author
    extra = 0

class SourceInline(admin.TabularInline):
    model = Source
    extra = 0

class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 0
class ArticleAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['url', 'title', 'influence']}),
		('Date information', {'fields': ['date_added', 'date_published']})
		]

	inlines = [AuthorInline, SourceInline, KeywordInline]

	list_display = ('title', 'url', 'influence', 'date_published', 'date_added')

admin.site.register(Article, ArticleAdmin)
