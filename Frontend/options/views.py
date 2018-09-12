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
    if request.method == 'POST':
        try:
            scopefile = request.FILES['scopefile']
            try:
                version = scopefile.readline().strip()
                db_version = common.get_config()['database']['version']
                if (version.count(".") == 2 and version != db_version):
                    result = format("Database schema version mismatch (Need: %s, Given: %s)" %
                                    (db_version, version))
                else:
                    # Backup Current Scope in a variable
                    out = StringIO()
                    management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)
                    currentScope = out.getvalue()
                    out.close()
                    
                    # Delete Current Scope
                    deleteScope()
                    deleted = True

                    # Replace Scope
                    tf = tempfile.NamedTemporaryFile(suffix='.json')
                    tf.write(scopefile.read())
                    tf.seek(0)
                    out = StringIO()
                    management.call_command('loaddata', tf.name, stdout=out)
                    out.close()
                    tf.close()
                    result = "Success"
            except:
                result = "Failed"
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
