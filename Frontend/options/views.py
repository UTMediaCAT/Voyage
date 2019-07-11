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
                    deleteAllScope()
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
                # if (allowed_file(scopefile, ALLOWED_EXTENSIONS_EXCEL) == False):
                #     raise ValueError('Wrong file type')

                # convert excel to json
                # call function to get json file
                # scopefile = convertFile(scopefile)

                # Backup Current Scope in a variable
                out = StringIO()
                management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)       # ????????????????????
                currentScope = out.getvalue()
                out.close()

                # read json file one by one
                jsonstr = scopefile.read().decode("utf-8")
                jsonDict = json.loads(jsonstr)
                result = ""
                skipped = []
                i = 0
                temp = []

                if (selected_type == "replace"):
                    # Delete Current Scope
                    deleteScopeSite()           # ????????????????????????????????????
                    deleted = True

                    # check if it's in source
                    for type in jsonDict.keys():
                        if "source" in type.lower():
                            # for every obj, add into source site db
                            src = jsonDict[type]
                            for subobj in src.keys():
                                obj = src[subobj]
                                for eachobj in obj:
                                    i = i + 1
                                    website = eachobj["Website"]
                                    sitename = eachobj["Outlet Name"]
                                    # newstype = obj["Type"]

                                    try:
                                        # add to source
                                        s = SourceSite(url=website, name=sitename)
                                        s.save()
                                    except:
                                        skipped.append(i)
                            
                        elif "referring" in type.lower():
                            # for every obj, add into referring site db
                            src = jsonDict[type]
                            for subobj in src.keys():
                                obj = src[subobj]
                                for eachobj in obj:
                                    i = i + 1
                                    website = eachobj["Website"]
                                    sitename = eachobj["Outlet Name"]
                                    default_scan = 2

                                    try:
                                        # add to referring
                                        r = ReferringSite(url=website, name=sitename, mode=default_scan, is_shallow=False)
                                        r.save()
                                    except:
                                        skipped.append(i)

                    result = "Successfully replaced"
                    if (len(skipped) > 0):
                        result += ", with skipped record of line "
                        result += str(skipped)

                elif (selected_type == "append"):
                    skippedException = []
                    # get info to insert to scope
                    for type in jsonDict.keys():
                        if "source" in type.lower():
                            # for every obj, add into source site db
                            src = jsonDict[type]
                            for subobj in src.keys():
                                obj = src[subobj]
                                for eachobj in obj:
                                    i = i + 1
                                    website = eachobj["Website"]
                                    sitename = eachobj["Outlet Name"]
                                    try:
                                        try:
                                            SourceSite.objects.get(url=website)
                                            skipped.append(i)
                                        except SourceSite.DoesNotExist:
                                            # add if does not exist
                                            s = SourceSite(url=website, name=sitename)
                                            s.save()
                                    except:
                                        skippedException.append(i)

                        elif "referring" in type.lower():
                            # for every obj, add into referring site db
                            src = jsonDict[type]
                            for subobj in src.keys():
                                obj = src[subobj]
                                for eachobj in obj:
                                    i = i + 1
                                    website = eachobj["Website"]
                                    sitename = eachobj["Outlet Name"]
                                    default_scan = 2 # both scan
                                    try:
                                        try:
                                            ReferringSite.objects.get(url=website)
                                            skipped.append(i)
                                        except ReferringSite.DoesNotExist:
                                            # add if does not exist
                                            r = ReferringSite(url=website, name=sitename, mode=default_scan, is_shallow=False)
                                            r.save()
                                    except:
                                        skippedException.append(i)

                    result = "Successfully appended"
                    if (len(skipped) > 0):
                        result += ", with duplicated skipped website of line "
                        result += str(skipped)
                    if (len(skippedException) > 0):
                        result += " , with error occurred skipped website of line "
                        result += str(skippedException)

            # except ValueError as e:
            #     result = "Wrong file type"
            except Exception as e:
                result = "Failed "
                result += str(e)
                restoreLastScope(deleted, currentScope)

            finally:
                context['scope_message_excel'] = result
        except:
            pass

    return render(request, 'options/downloads.html', context)

def uploadExcelTwitter(request):
    if not request.user.is_authenticated():
        return redirect('/admin/login/?next=%s' % request.path)

    deleted = False
    context = {}
    if request.method == 'POST':
        try:   # upload excel scope file
            scopefile = request.FILES['scopefileExcelTwitter']
            selected_type = request.POST['uploadType']
            try:
                # if (allowed_file(scopefile, ALLOWED_EXTENSIONS_EXCEL) == False):
                #     raise ValueError('Wrong file type')

                # convert excel to json
                # call function to get json file
                # scopefile = convertFile(scopefile)

                # Backup Current Scope in a variable
                out = StringIO()
                management.call_command('dumpdata', 'explorer', 'taggit', stdout=out)           # ?????????????????????
                currentScope = out.getvalue()
                out.close()

                # read json file one by one
                jsonstr = scopefile.read().decode("utf-8")
                jsonDict = json.loads(jsonstr)
                result = ""
                skipped = []
                i = 0
                temp = []

                if (selected_type == "replace"):
                    # Delete Current Scope
                    deleteScopeTwitter()        # ????????????????????????????????????
                    deleted = True

                    # get info to insert to scope
                    for obj in jsonDict:
                        i = i + 1
                        twitter_account = obj["Twitter Handle"]
                        sitename = obj["outlet name"]
                        site_type = obj["site_type"]
                        default_scan = 2 # both scanning method

                        # skip insert a record if exception happened when inserting
                        try:
                            # add if complete information
                            if (site_type == "sourcesite"):
                                # add to source
                                s = SourceSite(url=website, name=sitename)
                                s.save()

                            elif (site_type == "referringsite"):
                                # add to referring
                                r = ReferringSite(url=website, name=sitename, mode=default_scan, is_shallow=False)
                                r.save()
                            else:
                                raise Exception()
                        except:
                            skipped.append(i)

                    result = "Successfully replaced"
                    if (len(skipped) > 0):
                        result += ", with skipped record of line "
                        result += str(skipped)

                elif (selected_type == "append"):
                    skippedException = []
                    # get info to insert to scope
                    for obj in jsonDict:
                        i = i + 1
                        website = obj["website"]
                        sitename = obj["outlet name"]
                        site_type = obj["site_type"]
                        default_scan = 2 # both scan
                        try:
                            # add if complete information and no duplicate
                            if (site_type == "sourcesite"):
                                # check if there is the same existed source site & referring site
                                try:
                                    SourceSite.objects.get(url=website)
                                    skipped.append(i)
                                except SourceSite.DoesNotExist:
                                    # add if does not exist
                                    s = SourceSite(url=website, name=sitename)
                                    s.save()
                            elif (site_type == "referringsite"):
                                try:
                                    ReferringSite.objects.get(url=website)
                                    skipped.append(i)
                                except ReferringSite.DoesNotExist:
                                    # add if does not exist
                                    r = ReferringSite(url=website, name=sitename, mode=default_scan, is_shallow=False)
                                    r.save()
                            else:
                                raise Exception()
                        except:
                            skippedException.append(i)

                    result = "Successfully appened"
                    if (len(skipped) > 0):
                        result += ", with duplicated skipped website of line "
                        result += str(skipped)
                    if (len(skippedException) > 0):
                        result += " , with error occurred skipped website of line "
                        result += str(skippedException)

            # except ValueError as e:
            #     result = "Wrong file type"
            except:
                result = "Failed123"
                restoreLastScope(deleted, currentScope)

            finally:
                context['scope_message_exceltwitter'] = result
        except:
            pass

    return render(request, 'options/downloads.html', context)

def deleteAllScope():
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

def deleteScopeSite():
    ReferringSite.objects.all().delete()
    ReferringSiteFilter.objects.all().delete()
    SourceSite.objects.all().delete()
    SourceSiteAlias.objects.all().delete()
    # Keyword.objects.all().delete()
    # Tag.objects.all().delete()
    # TaggedItem.objects.all().delete()

def deleteScopeTwitter():
    ReferringSiteCssSelector.objects.all().delete()
    ReferringTwitter.objects.all().delete()
    SourceTwitter.objects.all().delete()
    SourceTwitterAlias.objects.all().delete()
    # Keyword.objects.all().delete()
    # Tag.objects.all().delete()
    # TaggedItem.objects.all().delete()

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
