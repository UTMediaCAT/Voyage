from django.contrib import admin
from libraries.nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from libraries.advanced_filters.admin import AdminAdvancedFiltersMixin
from articles.models import Article, Version, Author, SourceSite, Keyword, SourceTwitter
from django.utils.html import format_html

import re
# Register your models here.

import yaml, os
import common
import difflib


class AuthorInline(NestedStackedInline):
    model = Author
    fields = ['name']
    fk_name = 'version'
    extra = 0

# class SourceSiteInline(NestedTabularInline):
#     model = SourceSite
#     fields  = ('url', 'domain', 'anchor_text', 'matched', 'local',)
#     readonly_fields = ('url', 'domain', 'anchor_text', 'matched', 'local',)
#     fk_name = 'version'
#     extra = 0
#     verbose_name_plural = "Source URLs"

#     def has_add_permission(self, request):
#         return False

class KeywordInline(NestedTabularInline):
    model = Keyword
    readonly_fields = ('name',)
    fk_name = 'version'
    extra = 0

    def has_add_permission(self, request):
        return False

class SourceTwitterInline(NestedTabularInline):
    model = SourceTwitter
    verbose_name = "Source Tweet"
    verbose_name_plural = "Source Tweets"
    readonly_fields = ('name', 'matched',)
    fk_name = 'version'
    extra = 0

    def has_add_permission(self, request):
        return False

class VersionInline(NestedStackedInline):
    fieldsets = (
        (None, {
            'fields': ('title', 'highlighted_text', 'text_hash', 'language', 'date_added', 'date_last_seen', 'date_published', 'found_by', 'download_options',)
        }),
        # ('Source URLs', {
        #     'fields': ( 'source_url' , 'source_anchor_text', 'source_matched', 'source_local' )
        # }),
    )
    model = Version
    readonly_fields = ('highlighted_text', 'text_hash', 'date_added', 'date_last_seen', 'found_by', 'download_options',)
    inlines = [AuthorInline, KeywordInline]
    extra = 0
    
    def download_options(self, obj):

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        config = common.get_config()
        warc_file = root_dir + "/" + config['warc']['dir'] + "/" + config['warc']['article_subdir'] + "/" + obj.text_hash + ".warc.gz"
        warc_available = os.path.isfile(warc_file)

        pdf_file = root_dir + "/" + config['pdf']['dir'] + "/" + config['pdf']['article_subdir'] + "/" + obj.text_hash + ".pdf"
        pdf_available = os.path.isfile(pdf_file)

        img_file = root_dir + "/" + config['pdf']['dir'] + "/" + config['pdf']['article_subdir'] + "/" + obj.text_hash + ".png"
        img_available = os.path.isfile(img_file)
        # return format((
        #     """
        #     <div class="btn-group"> \
        #         <button class="btn btn-default" %s><a href="/articles/warc/%s">Download Warc</a></button> \
        #         <button class="btn btn-default" %s><a href="/articles/pdf/%s">View PDF</a></button> \
        #         <button class="btn btn-default" %s><a href="/articles/img/%s">View Screenshot</a></button> \
        #     </div> \
        #     """) %
        #     (
        #         '' if warc_available else 'disabled', obj.text_hash,
        #         '' if pdf_available else 'disabled', obj.text_hash,
        #         '' if img_available else 'disabled', obj.text_hash,
        #     ))

        return format_html((
            """
            <div class="btn-group"> \
                <a class="btn btn-success %s" %s>Download Warc</a> \
                <a class="btn btn-success %s" target="_blank" %s>View PDF</a> \
                <a class="btn btn-success %s" target="_blank" %s>View Screenshot</a> \
            </div> \
            """) %
            (
                '' if warc_available else 'disabled', 'href="/articles/warc/' + obj.text_hash + '"' if warc_available else '',
                '' if pdf_available else 'disabled', 'href="/articles/pdf/' + obj.text_hash + '"' if pdf_available else '',
                '' if img_available else 'disabled', 'href="/articles/img/' + obj.text_hash + '"' if img_available else '',
            ))
    download_options.short_description = "Download Options"

    def has_add_permission(self, request):
            return False

    def highlighted_text(self, obj):
        tag_front=" <strong><mark>"
        tag_end = "</mark></strong> "
        text = obj.text
        versions = list(obj.article.version_set.all())
        index = versions.index(obj)
        if (index > 0 and len(versions) - 1 >= index):
            prev_text = versions[index - 1].text
            diff = ''
            for line in difflib.unified_diff(re.split('(\s|\n)', prev_text), re.split('(\s|\n)', text), n=10000):
                for prefix in ('---', '+++', '@@'):
                    if line.startswith(prefix):
                        break
                else:
                    if '\n' in line:
                        if line[0] == '+' or line[0] == '-':
                            diff += line[1:]
                        else:
                            diff += line
                    elif line[0] == '+':
                        diff += ' <span style="background-color: CornflowerBlue"><strong> ' + line[1:] + ' </strong>&nbsp;</span>'
                    elif line[0] == '-':
                        diff += ' <span style="text-decoration: line-through"> ' + line[1:] + ' &nbsp;</span> '
                    else:
                        diff += line
            text = diff
        for key in obj.keyword_set.all():
            pattern = re.compile('([^a-z]' + key.name + '[^a-z])', re.IGNORECASE)
            result = pattern.subn(tag_front+key.name+tag_end, text)
            text = result[0]
        return '<div style="font-size: 1.2em">' + text + '</div>'

    highlighted_text.short_description = 'Text'

class ArticleAdmin(AdminAdvancedFiltersMixin, NestedModelAdmin):

    def get_queryset(self, request):
        return self.model.objects.filter(is_referring = True)
    
    fieldsets = [
        ('Basic',               {'fields': ('id', 'domain', 'show_urls')
        }
        ),
        ('Source Articles', {'fields': ['get_sources_info'] #('get_source_url', ('get_source_matched', 'get_source_local', 'get_source_anchor_text'))
        }
        )
        ]

    inlines = [VersionInline]

    list_display = ('get_url', 'title', 'get_authors', 'get_keywords', 'get_source_url', 'get_language', 'get_date_added', 'get_date_published', 'get_date_last_seen', 'link_options')
    search_fields = ['version__text','version__title']
    advanced_filter_fields = (
        'domain',
        'version__sourcesite__domain',
        'title',
        'version__language',
        ('version__keyword__name', 'Keyword'),
        ('version__sourcetwitter__name', 'Source Twitter'),
        ('version__date_added', 'Date Added'),
        ('version__date_published', 'Date Published'),
        ('version__date_last_seen', 'Date Last Seen'),
        ('version__text', 'Text'),
        ('version__title', 'Title'),
        ('version__author__name', 'Author'),
    )
    list_filter = ('domain', 'version__keyword__name', 'version__sourcesite__domain', 'version__sourcetwitter__name', 'version__language')
    readonly_fields = ('id', 'url', 'domain', 'title', 'language', 'found_by', 'date_added', 'date_last_seen', 'date_published', 'text', 'highlighted_text', 'show_urls', 'text_hash', 'get_source_url', 'get_source_matched', 'get_source_local', 'get_source_anchor_text', 'get_sources_info')
    actions_on_top = True
    list_per_page = 20



    def get_url(self, obj):
        link_short = obj.url
        if len(link_short) > 50:
            link_short = link_short[:50]+"..."
        return format('<a href="%s" target="_blank">%s</a>' % (obj.url, link_short))

    get_url.short_description = 'URL'
    get_url.admin_order_field = 'domain'
    get_url.allow_tags = True

    def get_authors(self, obj):
        authors = ''
        for ath in obj.version_set.last().author_set.all():
            authors += ath.name + ', '
        return authors[:-2]

    get_authors.short_description = 'Authors'

    def get_keywords(self, obj):
        keywords = ''
        for key in obj.version_set.last().keyword_set.all():
            keywords += key.name + ',<br>'
        return keywords[:-5]

    get_keywords.short_description = 'Matched Keywords'
    get_keywords.admin_order_field = 'version__keyword__name'
    get_keywords.allow_tags = True

    def get_source_matched(self, obj):

        match = ''
        for src in obj.sources.all():
            if (src.version_set.last().sourcesite_set.last().matched):
                match += '<img src="/static/admin/img/icon-yes.gif" alt="True" style="margin:5px; display:block">'
            else:
                match += '<img src="/static/admin/img/icon-no.gif" alt="False" style="margin:5px; display:block">'
        return match

    get_source_matched.short_description = 'Local'
    get_source_matched.admin_order_field = 'version__sourcesite__matched'
    get_source_matched.allow_tags = True

    def get_source_anchor_text(self, obj):

        anchors = ''
        for src in obj.sources.all():
            anchors += src.version_set.last().sourcesite_set.last().anchor_text
            anchors += '<br>'
        return anchors

    get_source_anchor_text.short_description = 'Anchor'
    get_source_anchor_text.admin_order_field = 'version__sourcesite__anchor__text'
    get_source_anchor_text.allow_tags = True

    def get_source_local(self, obj):

        local = ''
        for src in obj.sources.all():
            if (src.version_set.last().sourcesite_set.last().local):
                local += '<img src="/static/admin/img/icon-yes.gif" alt="True" style="margin:5px; display:block">'
            else:
                local += '<img src="/static/admin/img/icon-no.gif" alt="False" style="margin:5px; display:block">'
        return local

    get_source_local.short_description = 'Matched'
    get_source_local.admin_order_field = 'version__sourcesite__local'
    get_source_local.allow_tags = True

    def get_source_url(self, obj):
        sources = ''
        for src in obj.sources.all():
            if 'http://www.' in src.version_set.last().sourcesite_set.last().url:
                link = 'http://' + src.version_set.last().sourcesite_set.last().url[11:]
            else:
                link = src.version_set.last().sourcesite_set.last().url
            link_short = link[7:]
            if len(link_short) > 30:
                link_short = link_short[:30]+"..."

            sources += format('<a href="%s" target="_blank">%s</a>' % (link, link_short))
            sources += '<br>'
        return sources[:-4]

    def get_sources_info(self, obj):
        text = """</span><div id="src-info" style="margin-top:-25px;"><div style="display:flex;">
                    <div style="width:32%;display:flex;justify-content:center;align-items:center;">
                        <label style="margin:0;padding-right:0;width: auto;font-weight: 500 !important;">URL</label>
                    </div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Local</label>
                    </div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Matched</label>
                    </div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Anchor Text</label>
                    </div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Article Link</label>
                    </div>
                </div>"""

        

        for src in obj.sources.all():
            text += """<div style="display:flex;border-top: 1px solid #cccccc;margin-top: 4px;
                        padding-top: 4px;">
                        <div style="width:32%;display:flex;justify-content:center;align-items:center;">"""
            if 'http://www.' in src.version_set.last().sourcesite_set.last().url:
                link = 'http://' + src.version_set.last().sourcesite_set.last().url[11:]
            else:
                link = src.version_set.last().sourcesite_set.last().url
            link_short = link[7:]
            if len(link_short) > 30:
                link_short = link_short[:30]+"..."

            #text += format('<a href="%s" target="_blank" style="float:left;">%s</a>' % (link, link_short))
            text += '<a href="'+link+'" target="_blank">'+link_short+'</a>'
            text += """</div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">"""
            if (src.version_set.last().sourcesite_set.last().local):
                text += '<img src="/static/admin/img/icon-yes.gif" alt="True">'
            else:
                text += '<img src="/static/admin/img/icon-no.gif" alt="False">'

            text += """</div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">"""

            if (src.version_set.last().sourcesite_set.last().matched):
                text += '<img src="/static/admin/img/icon-yes.gif" alt="True">'
            else:
                text += '<img src="/static/admin/img/icon-no.gif" alt="False">'
            
            text += """</label>
                    </div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;text-align:center;overflow-x:auto;">"""

            text += '<p style="margin:0;padding:0;">' + src.version_set.last().sourcesite_set.last().anchor_text + '</p>'
            text += """</div>
                    <div style="width:17%;display:flex;align-items:center;justify-content:center;">
                        <a href=\"/admin/articles/sourcedarticle/""" + str(src.id)      + "\">"

            text += """ID: """ + str(src.id) + """ &#x2197;</a>
                        </div>
                    </div>"""

        text += """</div></span>"""
        return text

    get_source_url.short_description = 'Sourced URL'
    get_source_url.admin_order_field = 'version__sourcesite__url'
    get_source_url.allow_tags = True

    get_sources_info.short_description = 'Source Info'
    get_sources_info.admin_order_field = 'version__sourcesite__information'
    get_sources_info.allow_tags = True

  #   def get_source_twitters(self, obj):
  #       accounts = ''
  #       for acc in obj.version_set.last().sourcetwitter_set.all():
  #           if acc.matched:
        # accounts += acc + '<br>'
  #       return accounts[:-4]

  #   get_source_twitters.short_description = 'Matched Source Twitter Accounts'
  #   get_source_twitters.allow_tags = True

    def get_language(self, obj):
        return obj.language

    get_language.short_description = 'Language'
    get_language.admin_order_field = 'version__language'
    get_language.allow_tags = True

    def get_date_added(self, obj):
        return obj.date_added

    get_date_added.short_description = 'Date Added'
    get_date_added.admin_order_field = 'version__date_added'
    get_date_added.allow_tags = True

    def get_date_published(self, obj):
        return obj.date_published

    get_date_published.short_description = 'Date Published'
    get_date_published.admin_order_field = 'version__date_published'
    get_date_published.allow_tags = True

    def get_date_last_seen(self, obj):
        return obj.date_last_seen

    get_date_last_seen.short_description = 'Date Last Seen'
    get_date_last_seen.admin_order_field = 'version__date_last_seen'
    get_date_last_seen.allow_tags = True

    def highlighted_text(self, obj):
        tag_front=" <strong><mark>"
        tag_end = "</mark></strong> "
        text = obj.text
        for key in obj.version_set.last().keyword_set.all():
            pattern = re.compile('([^a-z]' + key.name + '[^a-z])', re.IGNORECASE)
            result = pattern.subn(tag_front+key.name+tag_end, text)
            text = result[0]
        return text

    highlighted_text.short_description = 'Highlighted Text'
    highlighted_text.allow_tags = True

    def show_urls(self, obj):
        urls = ''
        for url in obj.url_set.all():
            urls += format('<a href="%s" target="_blank">%s</a><br />' % (url.name, url.name))
        return urls

    show_urls.short_description = 'URLs'
    show_urls.allow_tags = True

    def link_url(self, obj):
        return format('<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url))

    link_url.allow_tags = True
    link_url.admin_order_field = 'url'
    link_url.short_description = "URL"

    def link_options(self, obj):
        return format((
            '<a href="/admin/articles/article/%s">Details</a><br />' +\
            '<div>Urls: %i<br />Versions: %i</div>') %
            (
                str(obj.pk),
                obj.url_set.count(),
                obj.version_set.count()))

    link_options.allow_tags = True
    link_options.short_description = "Options"


def create_modeladmin(modeladmin, model, name = None, menu_name = None):
    class  Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name = menu_name

    attrs = {'__module__': '', 'Meta': Meta}

    newmodel = type(name, (model,), attrs)

    admin.site.register(newmodel, modeladmin)
    return modeladmin

class SourcedArticleAdmin(ArticleAdmin):

    fieldsets = [
        ('Basic',               {'fields': ['id', 'domain', 'show_urls']}),
        ('Referring Articles', {'fields': ['get_referrals_info']})
        ]
    
    list_display = ('get_url', 'title', 'get_authors', 'get_keywords', 'get_referring_articles', 'get_language', 'get_date_added', 'get_date_published', 'get_date_last_seen', 'link_options')
    
    inlines = [VersionInline]
    
    def get_queryset(self, request):
        return self.model.objects.filter(is_source = True)

    search_fields = ['version__text','version__title']
    advanced_filter_fields = (
        'domain',
        'version__sourcesite__domain',
        'title',
        'version__language',
        ('version__keyword__name', 'Keyword'),
        ('version__sourcetwitter__name', 'Source Twitter'),
        ('version__date_added', 'Date Added'),
        ('version__date_published', 'Date Published'),
        ('version__date_last_seen', 'Date Last Seen'),
        ('version__text', 'Text'),
        ('version__title', 'Title'),
        ('version__author__name', 'Author'),
    )
    list_filter = ('domain', 'version__keyword__name', 'version__sourcesite__domain', 'version__sourcetwitter__name', 'version__language')
    readonly_fields = ('id', 'url', 'domain', 'title', 'language', 'found_by', 'date_added', 'date_last_seen', 'date_published', 'text', 'highlighted_text', 'show_urls', 'text_hash', 'get_referrals_info')
    actions_on_top = True
    list_per_page = 20

    def get_referrals_info(self, obj):
        text = """</span><div id="ref-info" style="margin-top:-25px;"><div style="display:flex;">
                    <div style="width:40%;display:flex;justify-content:center;align-items:center;">
                        <label style="margin:0;padding-right:0;width: auto;font-weight: 500 !important;">URL</label>
                    </div>
                    <div style="width:20%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Local</label>
                    </div>
                    <div style="width:20%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Matched</label>
                    </div>
                    <div style="width:20%;display:flex;align-items:center;justify-content:center;">
                        <label style="margin:0;padding-right:0;width:auto;font-weight: 500 !important;">Article Link</label>
                    </div>
                </div>"""

        

        for ref in obj.referrals.all():
            text += """<div style="display:flex;border-top: 1px solid #cccccc;margin-top: 4px;padding-top: 4px;">
                        <div style="width:40%;display:flex;justify-content:center;align-items:center;">"""
            if 'http://www.' in ref.url_set.last().name:
                link = 'http://' + ref.url_set.last().name[11:]
            else:
                link = ref.url_set.last().name
            link_short = link[8:]
            if len(link_short) > 40:
                link_short = link_short[:40]+"..."

            #text += format('<a href="%s" target="_blank" style="float:left;">%s</a>' % (link, link_short))
            text += '<a href="'+link+'" target="_blank">'+link_short+'</a>'
            text += """</div>"""
            count = 0
            for source in obj.version_set.last().sourcesite_set.all():
                #text += """<div>BLAH {count} </div>""".format(count=count) 
                count = count + 1
                #text += "<div>THIS IS A TEST</div>"

                # if 'http://www.' in source.referring_url:
                #     check_url = source.referring_url[11:]
                # elif 'https://www.' in source.referring_url:
                #     check_url = source.referring_url[12:]
                # elif 'http://' in source.referring_url:
                #     check_url = source.referring_url[7:]
                # elif 'https://' in source.referring_url:
                #     check_url = source.referring_url[8:]
                # else:
                check_url = source.referring_url
                #text += "<p>" + check_url + " *** " + ref.url + "</p>"

                domain = check_url.replace("https://www", "").replace("http://wwww", "")
                #text += "<p>" + domain + "</p>"
                # text += "<p>" + source.referring_url + " *** " + ref.url + "</p>"

                # text += """<div>""" + source.referring_url + """</div>"""
                # text += """<div>""" + ref.url + """</div>"""
                if source.referring_url in ref.url:
                    # text += """<div>""" + source.referring_url + """</div>"""
                    # text += """<div>""" + ref.url + """</div>"""
                    if source.local:
                        text += """<div style="width:20%;display:flex;align-items:center;justify-content:center;">
                                <img src="/static/admin/img/icon-yes.gif" alt="True">
                            </div>"""
                    else:
                        text += """<div style="width:20%;display:flex;align-items:center;justify-content:center;">
                                <img src="/static/admin/img/icon-no.gif" alt="False">
                            </div>"""
                    
                    if source.matched:
                        text += """<div style="width:20%;display:flex;align-items:center;justify-content:center;">
                                <img src="/static/admin/img/icon-yes.gif" alt="True">
                            </div>"""
                    else:
                        text += """<div style="width:20%;display:flex;align-items:center;justify-content:center;">
                                <img src="/static/admin/img/icon-no.gif" alt="False">
                            </div>"""
                    break



            text += """<div style="width:20%;display:flex;align-items:center;justify-content:center;">
                        <a href=\"/admin/articles/article/""" + str(ref.id)      + "\">"

            text += """ID: """ + str(ref.id) + """ &#x2197;
                        </a>
                         </div>
                     </div>"""


        text += """</div><span>"""
        return text

    get_referrals_info.short_description = 'Referrals Info'
    get_referrals_info.admin_order_field = 'version__referrals__information'
    get_referrals_info.allow_tags = True


    # override
    def link_options(self, obj):
        return format((
            '<a href="/admin/articles/sourcedarticle/%s">Details</a><br />' +\
            '<div>Urls: %i<br />Versions: %i</div>') %
            (
                str(obj.pk),
                obj.url_set.count(),
                obj.version_set.count()))

    link_options.allow_tags = True
    link_options.short_description = "Options"


    def get_referring_articles(self, obj):
        links = ''
        for ref in obj.referrals.all():
            links += format((
            '<a href="/admin/articles/article/%s">%s</a><br />') %
            (
                str(ref.pk),
                ref.title))
        return links

    get_referring_articles.short_description = 'Referring Articles'
    get_referring_articles.admin_order_field = 'version__referringarticle__url'
    get_referring_articles.allow_tags = True


create_modeladmin(SourcedArticleAdmin, name='sourcedarticle', model=Article, menu_name='Sourced Article')

admin.site.register(Article, ArticleAdmin)


# noinspection PyPackageRequirements,PyPackageRequirements
class SourceSiteAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Source Site', {
            'fields': ['url', 'domain','title', 'text_hash', 'language', 'date_added', 'date_last_seen', 'date_published', 'text', 
            ]})
        ]
    readonly_fields = ('url', 'domain', 'title','text_hash', 'language', 'date_added', 'date_last_seen', 'date_published', 'text')
    list_display = (['get_url','domain' , 'get_matched_article','get_source_author', 'get_referring_articles', 'get_source_date_added',  'get_source_date_published', 'link_options' ] )
    search_fields = [ 'url', 'domain','version__text','version__title' ]

    list_filter = ('domain', 'version__keyword__name', 'version__sourcetwitter__name', 'version__language')
    ordering = ['version__date_added']
    actions_on_top = True
    list_per_page = 20

    def get_referring_articles(self, obj):
        links = ''
        for ref in obj.version.article.referrals.all():
            links += format((
            '<a href="/admin/articles/article/%s">%s</a><br />') %
            (
                str(ref.pk),
                ref.title))
        return links
        # sources = ''
        # for ref in obj.version.article.referrals.all():
        #         if 'http://www.' in ref.url:
        #             link = 'http://' + ref.url[11:]
        #         else:
        #             link = ref.url
        #         link_short = link[7:]
        #         if len(link_short) > 30:
        #             link_short = link_short[:30]+"..."

        #         referrals += format('<a href="%s" target="_blank">%s</a>' % (link, link_short))
        #         referrals += '<br>'
        # return referrals[:-4]
        # return format((
        #     '<a href="/admin/articles/article/%s">Details</a><br />' +\
        #     '<div>Urls: %i<br />Versions: %i</div>') %
        #     (
        #         str(obj.pk),
        #         obj.url_set.count(),
        #         obj.version_set.count()))

    get_referring_articles.short_description = 'Referring Articles'
    get_referring_articles.admin_order_field = 'version__referringarticle__url'
    get_referring_articles.allow_tags = True

    def get_url(self, obj):
        link = obj.url.lstrip("/")
        if 'http://www.' in link:
            link = 'http://' + link[11:]

        link_short = link[7:]
        if len(link_short) > 30:
            link_short = link_short[:30]+"..."

        return format('<a href="%s" target="_blank">%s</a>' % (link, link_short))

    get_url.short_description = 'Source URL'
    get_url.admin_order_field = 'url'
    get_url.allow_tags = True

    def get_matched_article(self, obj):
        arctiles = ''
        source_set =  SourceSite.objects.filter(url=obj.url).order_by("version_id").distinct()
        existed_article_ids=set()
        for source in source_set:
            version =  Version.objects.get(id=source.version_id)
            arctile = Article.objects.get(id = version.article_id)
            if not arctile.id in existed_article_ids:
                existed_article_ids.add(arctile.id)
                arctiles += format('<a href="/admin/articles/article/%s">%s</a>' % (arctile.id, arctile.title))
                arctiles +=  '<br>'
        return arctiles[:-4]

    get_matched_article.short_description = 'Matched Articles'
    get_matched_article.admin_order_field = 'version__title'
    get_matched_article.allow_tags = True

    def get_source_author(self, obj):
        authors = ''

        source_set =  SourceSite.objects.filter(url=obj.url).order_by("version_id").distinct()
        existed_article_ids=set()
        for source in source_set:
            version =  Version.objects.get(id=source.version_id)
            arctile = Article.objects.get(id = version.article_id)
            if not arctile.id in existed_article_ids:
                existed_article_ids.add(arctile.id)
                au = ""
                for author in Author.objects.filter(version_id = version.id):
                        au += author.name + ', '

                authors += au +"<br>"

        return authors[:-2]

    get_source_author.short_description = 'Authors'
    get_source_author.allow_tags = True


    def get_source_date_added(self, obj):
        date_add = ''
        source_set =  SourceSite.objects.filter(url=obj.url).order_by("version_id").distinct()
        existed_article_ids=set()
        for source in source_set:
            version =  Version.objects.get(id=source.version_id)
            arctile = Article.objects.get(id = version.article_id)
            if not arctile.id in existed_article_ids:
                existed_article_ids.add(arctile.id)
                date_add += version.date_added.strftime("%B %d, %Y: %H:%M") + '<br>'

        return date_add[:-4]

    get_source_date_added.short_description = 'Date Added'
    get_source_date_added.admin_order_field = 'version__date_added'
    get_source_date_added.allow_tags = True

    def get_source_date_published(self, obj):
        date_published = ''
        source_set =  SourceSite.objects.filter(url=obj.url).order_by("version_id").distinct()
        existed_article_ids=set()
        for source in source_set:
            version =  Version.objects.get(id=source.version_id)
            arctile = Article.objects.get(id = version.article_id)
            if not arctile.id in existed_article_ids:
                existed_article_ids.add(arctile.id)
                date = version.date_published
                if not date:
                    date = ""
                else:
                    date = date.strftime("%B %d, %Y: %H:%M")
                date_published += date + '<br>'

        return date_published[:-4]

    get_source_date_published.short_description = 'Date Published'
    get_source_date_published.admin_order_field = 'version__date_published'

    get_source_date_published.allow_tags = True

    def link_options(self, obj):
        return format(('<a href="/admin/articles/sourcesite/%s">Details</a><br>') % obj.id)

    link_options.allow_tags = True
    link_options.short_description = "Options"

#to make each entry disinct in admin data list
'''
    def get_queryset(self, request):
        qs = super(SourceSiteAdmin, self).get_queryset(request)
        #qs = qs.filter(matched=True)
        qs = qs.order_by('url').distinct("url")
        return qs
'''

admin.site.register(SourceSite, SourceSiteAdmin)
