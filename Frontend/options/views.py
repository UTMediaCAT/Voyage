from django.shortcuts import render, redirect
from django.template import RequestContext, loader
from django.core import management
from subprocess import Popen
import sys, os
import tempfile
from io import StringIO
import common
import json

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

ALLOWED_EXTENSIONS_JSON = set(['json'])
ALLOWED_EXTENSIONS_EXCEL = set(['xlsx'])

def downloadPage(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    return render(request, 'options/downloads.html')

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
                if (str(version.count(bytes('.'.encode('utf-8')))) == 2 and version != db_version):
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
                    tf.write(bytes(scopefile.read()))
                    tf.seek(0)
                    out = StringIO()
                    management.call_command('loaddata', tf.name, stdout=out)
                    out.close()
                    tf.close()
                    result = "Success"
            except:
                result = "Failed"
                restoreLastScope(deleted, currentScope)
            finally:
                context['scope_message'] = result
        except:
            pass
    
    return render(request, 'options/downloads.html', context)

def downloadsExcel(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    deleted = False
    context = {}
    if request.method == 'POST':
        try:   # upload excel scope file
            scopefile = request.FILES['scopefileExcel']
            selected_type = request.POST['uploadType']
            try:
                version = scopefile.readline().strip()
                db_version = common.get_config()['database']['version']
                if (str(version.count(bytes('.'.encode('utf-8')))) == 2 and version != db_version):
                    result = format("Database schema version mismatch (Need: %s, Given: %s)" %
                                    (db_version, version))
                else:                    
                    # if (allowed_file(scopefile, ALLOWED_EXTENSIONS_EXCEL) == False):
                    #     raise ValueError('Wrong file type')

                    # convert excel to json
                    # call function to get json file

                    # Backup Current Scope in a variable
                    out = StringIO()
                    management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)
                    currentScope = out.getvalue()
                    out.close()
                    if (selected_type == "replace"):
                        # Delete Current Scope
                        deleteScope()
                        deleted = True

                        # Replace Scope
                        tf = tempfile.NamedTemporaryFile(suffix='.json')
                        tf.write(bytes(scopefile.read()))
                        tf.seek(0)
                        out = StringIO()
                        management.call_command('loaddata', tf.name, stdout=out)
                        out.close()
                        tf.close()
                        result = "Successfully replaced"
                      
                    elif (selected_type == "append"):
                        # Append Scope
                        tf = tempfile.NamedTemporaryFile(suffix='.json')
                        tf.write(bytes(scopefile.read()))
                        tf.seek(0)
                        out = StringIO()
                        management.call_command('loaddata', tf.name, stdout=out)
                        out.close()
                        tf.close()
                        result = "Successfully appended"
            # except ValueError as e:
            #     result = "Wrong file type"
            except:
                result = "Failed"
                restoreLastScope(deleted, currentScope)
                
            finally:
                context['scope_message_excel'] = result
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

def restoreLastScope(deleted, currentScope):
    if (deleted):
        # Put the Current Scope back into db
        tf = tempfile.NamedTemporaryFile('w+t', suffix='.json')
        try:
            with open(tf.name, 'w') as fd:
                fd.write(currentScope)
                fd.seek(0)
                management.call_command('loaddata', tf.name)
        finally:
            tf.close()

def allowed_file(filename, allowlist):
    return filename.split('.', 1)[1].lower() in allowlist