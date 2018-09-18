from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.core import management
from subprocess import Popen
import sys, os
import tempfile
from io import StringIO
import common

from explorer.models import (
    ReferringSite,
    ReferringSiteFilter,
    ReferringSiteCssSelector,
    ReferringTwitter,
    SourceTwitter,
    SourceTwitterAlias,
    SourceSite,
    SourceSiteAlias,
    Keyword
)
from taggit.models import (
    Tag,
    TaggedItem
)

def downloads(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    deleted = False
    context = {}
    result = "a"
    if request.method == 'POST':
        try:
            result += "b"
            scopefile = request.FILES['scopefile']
            try:
                result += "c"
                version = scopefile.readline().strip()
                db_version = common.get_config()['database']['version']
                result += "d"
                result += "DD"
                result += str(version.count(bytes('.'.encode('utf-8'))))
                result += "qqqqqq "
                if (str(version.count(bytes('.'.encode('utf-8')))) == 2 and version != db_version):
                    result += "d1"
                    result = format("Database schema version mismatch (Need: %s, Given: %s)" %
                                    (db_version, version))
                    result += "d2"
                else:
                    result += "e"
                    # Backup Current Scope in a variable
                    out = StringIO()
                    result += "f"
                    management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)
                    result += "g"
                    currentScope = out.getvalue()
                    out.close()
                    result += '1'
                    # Delete Current Scope
                    deleteScope()
                    deleted = True
                    result += ' 2'
                    # Replace Scope
                    tf = tempfile.NamedTemporaryFile(suffix='.json')
                    tf.write(bytes(scopefile.read()))
                    tf.seek(0)
                    out = StringIO()
                    result += ' 3'
                    management.call_command('loaddata', tf.name, stdout=out)
                    out.close()
                    tf.close()
                    result = "Success"
            except Exception as e:
                #result = "Faiadsasdasdad"
                result += repr(e)
                exc_type, exc_obj, exc_tb = sys.exc_info()
                result += str(exc_tb.tb_lineno)
                if (deleted):
                    # Put the Current Scope back into db
                    tf = tempfile.NamedTemporaryFile(suffix='.json')
                    tf.write(currentScope)
                    tf.seek(0)
                    management.call_command('loaddata', tf.name)
                    tf.close()
            finally:
                context['scope_message'] = result
        except:
            pass
    
    return render(request, 'options/downloads.html', context)

def deleteScope():
    ReferringSite.objects.all().delete()
    ReferringSiteFilter.objects.all().delete()
    ReferringSiteCssSelector.objects.all().delete()
    ReferringTwitter.objects.all().delete()
    SourceTwitter.objects.all().delete()
    SourceTwitterAlias.objects.all().delete()
    SourceSite.objects.all().delete()
    SourceSiteAlias.objects.all().delete()
    Keyword.objects.all().delete()
    Tag.objects.all().delete()
    TaggedItem.objects.all().delete()
