import os
import json

import locale
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse,HttpResponseRedirect, HttpResponseBadRequest,HttpResponseNotFound, \
    StreamingHttpResponse, JsonResponse
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from derisk.settings import *
from derisk_app.models import *
from derisk_app.forms import *
import datetime
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Count, Avg, CharField, Q, ForeignKey, ManyToManyField
from postgres_stats import Percentile
from django.db import connection
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import ugettext as _

# Create your views here.
from derisk_app.util.graphDesigner import get_field_policy, dictfetchall
from derisk_app.util.imports import import_excel, save_to_tmp
from derisk_app.util.importsverification import import_excelVerification, save_to_tmpVerification
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from derisk_app.util.json_encoder import DefaultEncoder


def index(request):
    return render(request, 'index.html')

@login_required
def privacyterms(request):
    return render(request, 'privacy-terms.html')

@login_required
def termsuse(request):
    return render(request, 'terms-use.html')

@login_required
def becomedataprovider(request):
    return render(request, 'becomedataprovider.html')


@login_required
def overview(request):

    locale.setlocale(locale.LC_NUMERIC, '')

    params = {}

    total_buildings = Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Building').count()
    total_industry = Project.objects.filter(sharing_level='ANA', istheinvestmentinabuilding_12='Industry').count()
    if total_buildings >0 and total_industry >0:

        locale.setlocale(locale.LC_NUMERIC, '')
        median_payback_industry = round(Project.objects.filter(indicator_simple_payback_time_AA__gt=0,sharing_level='ANA',istheinvestmentinabuilding_12='Industry').aggregate(median=Percentile('indicator_simple_payback_time_AA', 0.5, output_field=models.DecimalField()))['median'],1)
        median_payback_building = round(Project.objects.filter(indicator_simple_payback_time_AA__gt=0, sharing_level='ANA',istheinvestmentinabuilding_12='Building').aggregate(median=Percentile('indicator_simple_payback_time_AA', 0.5, output_field=models.DecimalField()))['median'], 1)
        avg_savings = '{0:n}'.format(int(round(Project.objects.filter(sharing_level='ANA').aggregate(Avg('indicator_energy_saved_AK'))['indicator_energy_saved_AK__avg'],0)))
        median_avoidance_industry = round(Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Industry',indicator_avoidance_cost0__gt=0).aggregate(median=Percentile('indicator_avoidance_cost0', 0.5, output_field=models.DecimalField()))['median'], 1)
        median_avoidance_building = round(Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Building',indicator_avoidance_cost0__gt=0).aggregate(median=Percentile('indicator_avoidance_cost0', 0.5, output_field=models.DecimalField()))['median'], 1)

        params['total_buildings'] = '{0:n}'.format(total_buildings)
        params['total_industry'] = '{0:n}'.format(total_industry)
        params['median_avoidance_industry'] = median_avoidance_industry
        params['median_payback_industry'] = median_payback_industry
        params['median_payback_building'] = median_payback_building
        params['median_avoidance_building'] = median_avoidance_building
        params['avg_savings'] = avg_savings

    return render(request, 'overview.html',params)

@login_required
def ProjectList(request):
    return render(request, 'project-list.html')

class ProjectUpdate(LoginRequiredMixin,UpdateView):
    def get_success_url(self):
        return '/projects/' + self.kwargs['pk']
    model = Project
    form_class = ProjectForm
    template_name = 'project-edit.html'

    def get_object(self, *args, **kwargs):
       obj = super(ProjectUpdate, self).get_object(*args, **kwargs)
       if obj.created_by != self.request.user:
         raise PermissionDenied() #or Http404
       return obj

class UserProfileView(LoginRequiredMixin,UpdateView):
    def get_success_url(self):
        return '/profile/edit/' + self.kwargs['pk']
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'userprofile-edit.html'
    context_object_name = 'userprofile'
    def get(self, *args, **kwargs):
        if (str(self.request.user.profile.id) != str(kwargs.get('pk'))):
            res = HttpResponse("Unauthorized")
            res.status_code = 401
            return res
        else:
            return super(UserProfileView, self).get(self, *args, **kwargs)

@login_required
def ProjectCreate(request, **kwargs):
    if request.method == 'POST':
        newProject = Project.objects.create(created_by = request.user)
    return HttpResponseRedirect('/projects/' + str(newProject.id))

@login_required
def ProjectDelete(request, **kwargs):
    if request.method == 'POST':
        selectedProject = Project.objects.filter(id=kwargs.get('pk'))[0]
        if (selectedProject.created_by  == request.user):
           selectedProject.delete()
    return HttpResponseRedirect('/projects')

@login_required
def ProjectSetAccessLevel(request, **kwargs):
    if request.method == 'POST':
       projectid = request.POST['projectid']
       sharinglevel = request.POST['sharinglevel']
       selectedProject = Project.objects.filter(id=projectid)[0]
       isVerified = request.user.groups.filter(name='verified_data_providers').count()>0
       isCreatedbyUser = selectedProject.created_by == request.user
       if (isCreatedbyUser & isVerified):
           selectedProject.sharing_level = sharinglevel
           selectedProject.save()
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       else:
          res = HttpResponse("Unauthorized")
          res.status_code = 401
          return res

@login_required
def ProjectUnlockAll(request, **kwargs):
    if request.method == 'POST':
       isVerified = request.user.groups.filter(name='verified_data_providers').count()>0
       if (isVerified):
           Project.objects.filter(created_by = request.user).update(sharing_level = 'ANA')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       else:
          res = HttpResponse("Unauthorized")
          res.status_code = 401
          return res

@login_required
def ProjectDeletePortfolio(request, **kwargs):
    if request.method == 'POST':
          Project.objects.filter(created_by = request.user).filter(sharing_level = 'PRI').delete()
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def ProjectLockAll(request, **kwargs):
    if request.method == 'POST':
       isVerified = request.user.groups.filter(name='verified_data_providers').count()>0
       if (isVerified):
           Project.objects.filter(created_by=request.user).update(sharing_level='PRI')
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       else:
          res = HttpResponse("Unauthorized")
          res.status_code = 401
          return res

@login_required
def upload_for_verification(request):
    ctx = {}

    if request.method == 'GET':
        ctx['form'] = UploadExcelForVerificationForm()
    elif request.method == 'POST':
        form = UploadExcelForVerificationForm(request.POST, request.FILES)
        if form.is_valid():
            # we need the file in the disk
            tmp_file = save_to_tmpVerification(request.FILES['excel_file'])
            msg = EmailMessage(
                  'DEEP Platform - Request for data verification in order to include it in the database',
                'Hi, <br> The following user has submitted the attached data in order to include it in the DEEP database<br>' + \
                  request.user.email + \
                 '<br>First Name:' + request.user.first_name + \
                 '<br>Last Name:' + request.user.last_name,
                DEFAULT_FROM_EMAIL,
                EMAILS_FOR_DATA_PROVIDERS,
            )
            msg.attach_file(tmp_file.name)
            msg.content_subtype = "html"
            msg.send()
            # import from the temporary file & return streaming response
            return StreamingHttpResponse(import_excelVerification(tmp_file.name, user=request.user), content_type='text/plain')

            return render(request, 'upload-for-verification.html', ctx)
        return HttpResponse('ERROR/%s' % form.errors['excel_file'][0])

    return render(request, 'upload-for-verification.html', ctx)

@login_required
def upload_from_excel(request):
    ctx = {}

    if request.method == 'GET':
        ctx['form'] = UploadExcelForm()
    elif request.method == 'POST':
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            # we need the file in the disk
            tmp_file = save_to_tmp(request.FILES['excel_file'])

            # import from the temporary file & return streaming response
            return StreamingHttpResponse(import_excel(tmp_file.name, user=request.user), content_type='text/plain')

        return HttpResponse('ERROR/%s' % form.errors['excel_file'][0])

    return render(request, 'upload-from-excel.html', ctx)


#Optimize for chart display
def displayOrganizationSize(text):
    if text == 'LARGE':
        return _('Large enterprises(250+ employees)')
    if text == 'MEDIUM':
        return _('Medium enterprises(50-249 employees)')
    if text == 'SMALL':
        return _('Small enterprises(10-49 employees)')
    if text == 'MICRO':
        return _('Micro enterprises(<10 employees)')
    return ''

@login_required
def ApiFactsheetNumberOfProjects(request):
    kwargs = {
    }
    if request.method == 'GET':
        kwargs['sharing_level'] = 'ANA'
        if 'projecttype' in request.GET.keys():
            if request.GET['projecttype'] != 'Industry':
                kwargs['istheinvestmentinabuilding_12'] = 'Building'
            else:
                kwargs['istheinvestmentinabuilding_12'] = 'Industry'
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                   kwargs['country_3__in'] = EU_COUNTRY_LIST
                else:
                   kwargs['country_3']=request.GET['country']
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                kwargs['measures_main'] = request.GET['measuretype']
        if 'companysize' in request.GET.keys():
            if request.GET['companysize'] != '':
                kwargs['organizationsize_14'] = request.GET['companysize']
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                kwargs['buildingtype_15'] = request.GET['buildingtype']
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                kwargs['verified_simple'] = request.GET['verification']
        # count number of projects
        chartQuery = Project.objects.filter(**kwargs).count()
        chart_data = []
        chart_data.append({'number_of_projects':chartQuery})

        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiBenchmarkNumberOfProjects(request):
    kwargs = {
    }
    if request.method == 'GET':
        kwargs['sharing_level'] = 'ANA'
        if 'projecttype' in request.GET.keys():
            if request.GET['projecttype'] != 'Industry':
                kwargs['istheinvestmentinabuilding_12'] = 'Building'
            else:
                kwargs['istheinvestmentinabuilding_12'] = 'Industry'
        if 'country' in request.GET.keys():
            if request.GET['country'] != '':
                if request.GET['country'] == 'EU':
                    kwargs['country_3__in'] = EU_COUNTRY_LIST
                else:
                    kwargs['country_3'] = request.GET['country']
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                kwargs['measures_main'] = request.GET['measuretype']
        if 'companysize' in request.GET.keys()  and request.GET['projecttype'] =='Industry':
            if request.GET['companysize'] != '':
                kwargs['organizationsize_14'] = request.GET['companysize']
        if 'buildingtype' in request.GET.keys() and request.GET['projecttype'] =='Building':
            if request.GET['buildingtype'] != '':
                kwargs['buildingtype_15'] = request.GET['buildingtype']
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                kwargs['verified_simple'] = request.GET['verification']
        # count number of projects
        chartQuery = Project.objects.filter(**kwargs).count()
        chart_data = []
        chart_data.append({'number_of_projects':chartQuery})
        # count number of portfolio projects
        kwargs = {
        }
        kwargs['created_by'] = request.user.id
        chartQuery = Project.objects.filter(**kwargs).count()
        chart_data.append({'number_of_projects_portfolio':chartQuery})

        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetIndustryCandleStickDistributionSize(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET['country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'companysize' in request.GET.keys():
            if request.GET['companysize'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."organizationsize_14" = \'' + request.GET['companysize'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Industry - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."organizationsize_14", COUNT("derisk_app_project"."indicator_simple_payback_time_AA") AS observations  ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Industry\' AND ' +\
                   '"derisk_app_project"."organizationsize_14" <> \'\' AND ' + \
                   '"derisk_app_project"."organizationsize_14" <> \'0\' AND ' + \
                   '"derisk_app_project"."indicator_simple_payback_time_AA" >0' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."organizationsize_14" ' + \
                   ' HAVING COUNT("derisk_app_project"."indicator_simple_payback_time_AA") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '
        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']
        chart_data = [{'category': displayOrganizationSize(d['organizationsize_14']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'low': round(d['low'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetIndustryCandleStickDistributionMeasures(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'companysize' in request.GET.keys():
            if request.GET['companysize'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."organizationsize_14" = \'' + request.GET['companysize'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Industry - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."measures_main", COUNT("derisk_app_project"."indicator_simple_payback_time_AA") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Industry\' AND ' +\
                   '"derisk_app_project"."indicator_simple_payback_time_AA" >0' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."measures_main" '  + \
                   ' HAVING COUNT("derisk_app_project"."indicator_simple_payback_time_AA")>= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '
        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': _(d['measures_main']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'low': round(d['low'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetIndustrySaving(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    kwargs = {
    }
    kwargs['istheinvestmentinabuilding_12'] = 'Industry'
    kwargs['sharing_level'] = 'ANA'
    kwargs['indicator_simple_payback_time_AA__gt'] = 0
    if request.method == 'GET':
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    kwargs['country_3__in'] = EU_COUNTRY_LIST
                else:
                    kwargs['country_3'] = request.GET['country']
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                kwargs['measures_main'] = request.GET['measuretype']
        if 'companysize' in request.GET.keys():
            if request.GET['companysize'] != '':
                kwargs['organizationsize_14'] = request.GET['companysize']
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                kwargs['verified_simple'] = request.GET['verification']
        # Industry Energy Saving Potential by average payback time
        chartQuery = Project.objects.filter(**kwargs) \
            .values('measures_main') \
            .annotate(Investment=Sum('valueofeeinvestment_51')) \
            .annotate(Energycostsaved=Sum('netannualsaving_55')) \
            .annotate(SumEnergySaved=Sum('indicator_energy_saved_AK') / 1000000) \
            .annotate(SimplePaybackTime=Avg('indicator_simple_payback_time_AA')) \
            .annotate(observations=Count('indicator_simple_payback_time_AA')) \
            .filter(observations__gt=request.user.userprofile.sample_size_limit) \
            .order_by('SimplePaybackTime')

        chart_data = []
        totalobservations = 0
        for obj in chartQuery:
            totalobservations = totalobservations + obj['observations']
        for obj in chartQuery:
            if obj['SumEnergySaved'] is not None:
                if obj['SumEnergySaved'] > 0:
                    chart_data.append({
                        'measures_main': _(obj['measures_main']),
                        'Investment': '{0:n}'.format(int(round(obj['Investment'],2))),
                        'Energycostsaved': '{0:n}'.format(round(obj['Energycostsaved'],2)),
                        'SumEnergySaved': round(obj['SumEnergySaved'],2),
                        'SumEnergySavedFormatted': '{0:n}'.format(round(obj['SumEnergySaved'], 2)),
                        'SimplePaybackTime': '{:,}'.format(round(obj['SimplePaybackTime'],2)),
                        'Color': dict(MEASURESTOCOLOR).get(obj['measures_main']),
                        'observations': '{0:n}'.format(obj['observations']),
                        'totalobservations': '{0:n}'.format(totalobservations),
                    })
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetIndustryCandleStickDistributionEURmwh(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'companysize' in request.GET.keys():
            if request.GET['companysize'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."organizationsize_14" = \'' + request.GET['companysize'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Industry - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        str_avoidance_indicator = 'indicator_avoidance_cost0'
        if 'discountrate' in request.GET.keys():
            if request.GET['discountrate'] != '':
                str_avoidance_indicator = request.GET['discountrate']
        my_query = 'SELECT "derisk_app_project"."measures_main", COUNT("derisk_app_project"."'+ str_avoidance_indicator +'") AS observations  ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."'+ str_avoidance_indicator +'" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."'+ str_avoidance_indicator +'" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."'+ str_avoidance_indicator +'" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."'+ str_avoidance_indicator +'" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."'+ str_avoidance_indicator +'" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Industry\' AND ' +\
                   '"derisk_app_project"."'+ str_avoidance_indicator +'" >0 ' + \
                   ' AND "derisk_app_project"."measures_main" <> \'\' ' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."measures_main" '+ \
                   ' HAVING COUNT("derisk_app_project"."'+ str_avoidance_indicator +'") >= ' + request.user.userprofile.sample_size_limit + \
                    ' ORDER BY median ASC '
        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']
        chart_data = [{'category': _(d['measures_main']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsSaving(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    kwargs = {
    }
    kwargs['istheinvestmentinabuilding_12'] = 'Building'
    kwargs['sharing_level'] = 'ANA'
    kwargs['indicator_simple_payback_time_AA__gt'] = 0
    if request.method == 'GET':
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    kwargs['country_3__in'] = EU_COUNTRY_LIST
                else:
                    kwargs['country_3'] = request.GET['country']
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                kwargs['measures_main'] = request.GET['measuretype']
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                kwargs['buildingtype_15'] = request.GET['buildingtype']
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                kwargs['verified_simple'] = request.GET['verification']
        # Buildings Energy Saving Potential by average payback time
        chartQuery = Project.objects.filter(**kwargs) \
            .values('buildingtype_15') \
            .annotate(Investment=Sum('valueofeeinvestment_51'), ) \
            .annotate(Energycostsaved=Sum('netannualsaving_55')) \
            .annotate(SumEnergySaved=Sum('indicator_energy_saved_AK') / 1000000) \
            .annotate(SimplePaybackTime=Avg('indicator_simple_payback_time_AA')) \
            .annotate(observations=Count('indicator_simple_payback_time_AA')) \
            .filter(observations__gt=request.user.userprofile.sample_size_limit) \
            .order_by('SimplePaybackTime')

        chart_data = []
        totalobservations = 0
        for obj in chartQuery:

            totalobservations = totalobservations + obj['observations']
        for obj in chartQuery:
            if obj['SumEnergySaved'] is not None and obj['Investment'] is not None:
                if obj['SumEnergySaved'] > 0:
                    if obj['buildingtype_15'] != '':
                        strBuildingType = dict(BUILDINGTYPE).get(obj['buildingtype_15'])
                    else:
                        strBuildingType = _('Not specified')
                    chart_data.append({
                        'buildingtype_15': strBuildingType,
                        'Investment': '{0:n}'.format(int(round(obj['Investment'],2))),
                        'Energycostsaved': round(obj['Energycostsaved'],2),
                        'SumEnergySaved': round(obj['SumEnergySaved'],2),
                        'SumEnergySavedFormatted': '{0:n}'.format(round(obj['SumEnergySaved'], 2)),
                        'SimplePaybackTime': round(obj['SimplePaybackTime'],2),
                        'Color': dict(BUILDINGTOCOLOR).get(obj['buildingtype_15']),
                        'observations': '{0:n}'.format(obj['observations']),
                        'totalobservations': '{0:n}'.format(totalobservations),
                    })
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)


@login_required
def ApiFactsheetBuildingsMeasure(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."measures_main", COUNT("derisk_app_project"."indicator_simple_payback_time_AA") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."indicator_simple_payback_time_AA" >0' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."measures_main" '  + \
                   ' HAVING COUNT("derisk_app_project"."indicator_simple_payback_time_AA") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '


        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': _(d['measures_main']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'low': round(d['low'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsMeasure2(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT finaltable.levelcode,ltrim(trim(both \'1234567890.\' from derisk_app_measure.title)) as title, finaltable.observations,finaltable.open,finaltable.high,finaltable.median,finaltable.low,finaltable.close FROM (' \
                   'SELECT substring("derisk_app_measure"."code" from 1 for 6) as LEVELCODE, COUNT(ONLY_ONCE."indicator_simple_payback_time_AA") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ONLY_ONCE."indicator_simple_payback_time_AA" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY ONLY_ONCE."indicator_simple_payback_time_AA" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY ONLY_ONCE."indicator_simple_payback_time_AA" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY ONLY_ONCE."indicator_simple_payback_time_AA" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ONLY_ONCE."indicator_simple_payback_time_AA" ASC) "close"  ' +\
                   ' FROM (' +\
                   'SELECT  derisk_app_project.id,"derisk_app_project"."indicator_simple_payback_time_AA"' +\
                   'FROM public.derisk_app_project, public.derisk_app_project_measures_18, public.derisk_app_measure  WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND  derisk_app_project_measures_18.project_id = derisk_app_project.id AND  derisk_app_project_measures_18.measure_id = derisk_app_measure.id AND "derisk_app_project"."indicator_simple_payback_time_AA" >0 ' + str_criteria + 'AND"derisk_app_project"."indicator_simple_payback_time_AA" <100  AND "derisk_app_project"."sharing_level" = \'ANA\'  GROUP BY derisk_app_project.id HAVING COUNT(derisk_app_project.id)=1' +\
                   ') AS ONLY_ONCE, "derisk_app_measure",derisk_app_project_measures_18 ' +\
                   ' WHERE ' + \
                   ' derisk_app_project_measures_18.project_id = ONLY_ONCE.id AND ' + \
                   ' derisk_app_project_measures_18.measure_id = derisk_app_measure.id ' + \
                   ' GROUP BY LEVELCODE '  + \
                   ' HAVING COUNT(ONLY_ONCE."indicator_simple_payback_time_AA") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC ' + \
                ') AS FINALTABLE, derisk_app_measure  where finaltable.levelcode = derisk_app_measure.code AND LENGTH(derisk_app_measure.code)=6'


        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': d['title'],
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'low': round(d['low'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)


@login_required
def ApiFactsheetBuildingsBuilding(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."buildingtype_15", COUNT("derisk_app_project"."indicator_simple_payback_time_AA") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."indicator_simple_payback_time_AA" >0' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."buildingtype_15" '  + \
                   ' HAVING COUNT("derisk_app_project"."indicator_simple_payback_time_AA") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '

        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': dict(BUILDINGTYPE).get(d['buildingtype_15']) if dict(BUILDINGTYPE).get(d['buildingtype_15']) !='' else _('Not Specified'),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsCandleStickDistributionEURmwh(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        str_avoidance_indicator = 'indicator_avoidance_cost0'
        if 'discountrate' in request.GET.keys():
            if request.GET['discountrate'] != '':
                str_avoidance_indicator = request.GET['discountrate']
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."measures_main", COUNT("derisk_app_project"."' + str_avoidance_indicator + '") AS observations  ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."' + str_avoidance_indicator + '" >0 ' + \
                   ' AND "derisk_app_project"."measures_main" <> \'\' ' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."measures_main"'  + \
                   ' HAVING COUNT("derisk_app_project"."' + str_avoidance_indicator + '") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '


        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': _(d['measures_main']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsCandleStickDistributionEURmwh2(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        str_avoidance_indicator = 'indicator_avoidance_cost0'
        if 'discountrate' in request.GET.keys():
            if request.GET['discountrate'] != '':
                str_avoidance_indicator = request.GET['discountrate']
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles

        my_query = 'SELECT finaltable.levelcode,ltrim(trim(both \'1234567890.\' from derisk_app_measure.title)) as title, finaltable.observations,finaltable.open,finaltable.high,finaltable.median,finaltable.low,finaltable.close FROM (' \
                   'SELECT substring("derisk_app_measure"."code" from 1 for 6) as LEVELCODE, COUNT(ONLY_ONCE."'+str_avoidance_indicator +'") AS observations ,' + \
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY ONLY_ONCE."'+str_avoidance_indicator +'" ASC) "open",' + \
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY ONLY_ONCE."'+str_avoidance_indicator +'" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY ONLY_ONCE."'+str_avoidance_indicator +'" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY ONLY_ONCE."'+str_avoidance_indicator +'" ASC) "low",' + \
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY ONLY_ONCE."'+str_avoidance_indicator +'" ASC) "close"  ' + \
                   ' FROM (' + \
                   'SELECT  derisk_app_project.id,"derisk_app_project"."'+str_avoidance_indicator +'"' + \
                   'FROM public.derisk_app_project, public.derisk_app_project_measures_18, public.derisk_app_measure  WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND  derisk_app_project_measures_18.project_id = derisk_app_project.id AND  derisk_app_project_measures_18.measure_id = derisk_app_measure.id AND "derisk_app_project"."'+str_avoidance_indicator +'" >0 ' + str_criteria + 'AND"derisk_app_project"."'+str_avoidance_indicator +'" <100  AND "derisk_app_project"."sharing_level" = \'ANA\'  GROUP BY derisk_app_project.id HAVING COUNT(derisk_app_project.id)=1' + \
                   ') AS ONLY_ONCE, "derisk_app_measure",derisk_app_project_measures_18 ' + \
                   ' WHERE ' + \
                   ' derisk_app_project_measures_18.project_id = ONLY_ONCE.id AND ' + \
                   ' derisk_app_project_measures_18.measure_id = derisk_app_measure.id ' + \
                   ' GROUP BY LEVELCODE ' + \
                   ' HAVING COUNT(ONLY_ONCE."'+str_avoidance_indicator +'") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC ' + \
                   ') AS FINALTABLE, derisk_app_measure  where finaltable.levelcode = derisk_app_measure.code AND LENGTH(derisk_app_measure.code)=6'

        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': d['title'],
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)


@login_required
def ApiFactsheetBuildingsCandleStickDistributionEURmwhBuilding(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        str_avoidance_indicator = 'indicator_avoidance_cost0'
        if 'discountrate' in request.GET.keys():
            if request.GET['discountrate'] != '':
                str_avoidance_indicator = request.GET['discountrate']
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."buildingtype_15", COUNT("derisk_app_project"."' + str_avoidance_indicator + '") AS observations  ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."' + str_avoidance_indicator + '" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."' + str_avoidance_indicator + '" >0 ' + \
                   ' AND "derisk_app_project"."buildingtype_15" <> \'\' ' + \
                    str_criteria + \
                   ' GROUP BY "derisk_app_project"."buildingtype_15"'  + \
                   ' HAVING COUNT("derisk_app_project"."' + str_avoidance_indicator + '") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC '
        cursor = connection.cursor()
        cursor.execute((my_query))
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': dict(BUILDINGTYPE).get(d['buildingtype_15']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsCandleStickDistributionEURm2(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."measures_main", COUNT("derisk_app_project"."indicator_EURm2_AU") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."indicator_EURm2_AU" >0' + \
                    str_criteria + \
                   ' AND "derisk_app_project"."measures_main" <> \'\' ' + \
                   ' GROUP BY "derisk_app_project"."measures_main"' + \
                   ' HAVING COUNT("derisk_app_project"."indicator_EURm2_AU") >= ' + request.user.userprofile.sample_size_limit +\
                   ' ORDER BY median ASC'

        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': _(d['measures_main']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiFactsheetBuildingsCandleStickDistributionEURm2Building(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    str_criteria = ''
    if request.method == 'GET':
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.GET.keys():
            if request.GET['country'] != '' :
                if request.GET['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.GET[
                        'country'] + '\''
        if 'measuretype' in request.GET.keys():
            if request.GET['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.GET['measuretype'] + '\''
        if 'buildingtype' in request.GET.keys():
            if request.GET['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.GET['buildingtype'] + '\''
        if 'verification' in request.GET.keys():
            if request.GET['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.GET['verification'] + '\''
        # Building - Distribution of payback time on 10%, 25%, 75% and 90% percentiles
        my_query = 'SELECT "derisk_app_project"."buildingtype_15", COUNT("derisk_app_project"."indicator_EURm2_AU") AS observations ,' +\
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "high",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "median",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_EURm2_AU" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'Building\' AND ' +\
                   '"derisk_app_project"."indicator_EURm2_AU" >0' + \
                    str_criteria + \
                   ' AND "derisk_app_project"."measures_main" <> \'\' ' + \
                   ' GROUP BY "derisk_app_project"."buildingtype_15"' + \
                   ' HAVING COUNT("derisk_app_project"."indicator_EURm2_AU") >= ' + request.user.userprofile.sample_size_limit + \
                   ' ORDER BY median ASC'

        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']

        chart_data = [{'category': dict(BUILDINGTYPE).get(d['buildingtype_15']),
                       'open': round(d['open'],2),
                       'high': round(d['high'],2),
                       'median': round(d['median'],2),'medianFormatted': '{0:n}'.format(round(d['median'],2)),
                       'low': round(d['low'],2),
                       'close': round(d['close'],2),
                       'observations': '{0:n}'.format(d['observations']),
                       'totalobservations': '{0:n}'.format(totalobservations),
                       } for d in raw_data]
        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiBenchmark(request):
    str_criteria = ''
    locale.setlocale(locale.LC_NUMERIC, '')
    benchmark_method = 'indicator_avoidance_cost0'
    if request.method == 'POST':
        if 'benchmarkmethod' in request.POST.keys() :
            benchmark_method = request.POST['benchmarkmethod']
            if 'discountrate' in request.POST.keys():
                if benchmark_method == 'indicator_avoidance_cost0':
                      benchmark_method = request.POST['discountrate']
        str_criteria = str_criteria + ' AND "derisk_app_project"."sharing_level" = \'ANA\''
        if 'country' in request.POST.keys():
            if request.POST['country'] != '' :
                if request.POST['country'] == 'EU':
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" IN ' + EU_COUNTRY_LIST_SQL
                else:
                    str_criteria = str_criteria + ' AND "derisk_app_project"."country_3" = \'' + request.POST['country'] + '\''
        if 'measuretype' in request.POST.keys():
            if request.POST['measuretype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."measures_main" = \'' + request.POST['measuretype'] + '\''
        if 'companysize' in request.POST.keys() and request.POST['projecttype'] == 'Industry':
            if request.POST['companysize'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."organizationsize_14" = \'' + request.POST['companysize'] + '\''
        if 'buildingtype' in request.POST.keys() and request.POST['projecttype'] == 'Building':
            if request.POST['buildingtype'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."buildingtype_15" = \'' + request.POST['buildingtype'] + '\''
        if 'verification' in request.POST.keys():
            if request.POST['verification'] != '':
                str_criteria = str_criteria + ' AND "derisk_app_project"."verified_simple" = \'' + request.POST['verification'] + '\''
        # Get chart for database selection
        my_query = 'SELECT  ' + \
                   'STDDEV_SAMP("derisk_app_project"."' + benchmark_method + '") AS "stddev",' + \
                   'COUNT("derisk_app_project"."' + benchmark_method + '") AS "observations",' + \
                   'AVG("derisk_app_project"."' + benchmark_method + '") AS "avg",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "median",' + \
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method +'" ASC) "open",' +\
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method +'" ASC) "high",' +\
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method +'" ASC) "low",' +\
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method +'" ASC) "close"  ' +\
                   'FROM "derisk_app_project" ' +\
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'' + request.POST['projecttype'] + '\' AND ' + \
                   '"derisk_app_project"."' + benchmark_method +'" >0' + \
                    str_criteria + \
                   ' ORDER BY median ASC '

        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)
        chart_data = []
        multiplier = 1
        totalobservations = 0
        for d in raw_data:
            totalobservations = totalobservations + d['observations']
        if benchmark_method == 'indicator_saving_pct_other_AS' or  benchmark_method == 'indicator_saving_pct_forecast_AL' or  benchmark_method == 'indicator_saving_pct_actual_AM':
            multiplier = 100
        for d in raw_data:
            d_open = None
            d_high = None
            d_low = None
            d_close = None
            d_avg = None
            d_stddev = None
            d_median = None
            d_center = None
            d_medianFormatted = None
            if d['open'] is not None:
                d_open = round(d['open'] * multiplier,2)
            if d['high'] is not None:
                d_high = round(d['high'] * multiplier,2)
            if d['low'] is not None:
                d_low = round(d['low'] * multiplier,2)
            if d['close'] is not None:
                d_close = round(d['close'] * multiplier,2)
            if d['avg'] is not None:
                d_avg = round(d['avg'] * multiplier,2)
            if d['stddev'] is not None:
                d_stddev = round(d['stddev'] * multiplier,2)
            if d['median'] is not None:
                d_median = round(d['median'] * multiplier,2)
                d_medianFormatted = '{0:n}'.format(round(d['median'] * multiplier,2))
            if d['open'] is not None and d['close'] is not None and d['low'] is not None:
                d_center = (d['open'] - d['close'] ) / 2 + d['close']
            chart_data.append({'category': _('Database selection'),
                           'open': d_open,
                           'high': d_high,
                           'low': d_low,
                           'close': d_close,
                           'avg': d_avg,
                           'stddev': d_stddev,
                            'median': d_median,
                               'medianFormatted': d_medianFormatted,
                           'observations' : d['observations'],
                            'center': d_center,
                           'totalobservations': totalobservations,
                            'samplesizelimit': request.user.userprofile.sample_size_limit,
                           })

        # Get chart for portfolio
        str_criteria = ''
        str_criteria = ' AND "derisk_app_project"."created_by_id" = ' + str(request.user.id)
        if 'selectedProjects[]' in request.POST.keys():
            selectedIDs = request.POST.getlist('selectedProjects[]')
            if len(selectedIDs) > 0:
                str_id_criteria = '('
                for curId in selectedIDs:
                    str_id_criteria = str_id_criteria + curId + ','
                str_id_criteria = str_id_criteria[:-1] + ')'
                str_criteria = str_criteria + ' AND "derisk_app_project"."id" in ' + str_id_criteria
        my_query = 'SELECT  ' + \
                   'STDDEV_SAMP("derisk_app_project"."' + benchmark_method + '") AS "stddev",' + \
                   'COUNT("derisk_app_project"."' + benchmark_method + '") AS "observations",' + \
                   'AVG("derisk_app_project"."' + benchmark_method + '") AS "avg",' + \
                   'PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "median",' + \
                   'PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "open",' + \
                   'PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "high",' + \
                   'PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "low",' + \
                   'PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "derisk_app_project"."' + benchmark_method + '" ASC) "close"  ' + \
                   'FROM "derisk_app_project" ' + \
                   ' WHERE "derisk_app_project"."istheinvestmentinabuilding_12" = \'' + request.POST['projecttype'] + '\' AND ' + \
                   '"derisk_app_project"."' + benchmark_method + '" >0' + \
                   str_criteria + \
                   ' ORDER BY median ASC'
        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)

        multiplier = 1
        if benchmark_method == 'indicator_saving_pct_other_AS' or  benchmark_method == 'indicator_saving_pct_forecast_AL' or  benchmark_method == 'indicator_saving_pct_actual_AM':
            multiplier = 100

        for d in raw_data:
            d_open = None
            d_high = None
            d_low = None
            d_close = None
            d_avg = None
            d_stddev = None
            d_median = None
            if d['open'] is not None:
                d_open = round(d['open'] * multiplier,2)
            if d['high'] is not None:
                d_high = round(d['high'] * multiplier,2)
            if d['low'] is not None:
                d_low = round(d['low'] * multiplier,2)
            if d['close'] is not None:
                d_close = round(d['close'] * multiplier,2)
            if d['avg'] is not None:
                d_avg = round(d['avg'] * multiplier,2)
            if d['stddev'] is not None:
                d_stddev = round(d['stddev'] * multiplier,2)
            if d['median'] is not None:
                d_median = round(d['median'] * multiplier,2)
                d_medianFormatted = '{0:n}'.format(round(d['median'] * multiplier,2))
            chart_data.append({'category': _('Your portfolio'),
                           'open': d_open,
                           'high': d_high,
                           'low': d_low,
                           'close': d_close,
                           'avg': d_avg,
                           'stddev': d_stddev,
                            'median': d_median,
                               'medianFormatted': d_medianFormatted,
                           'observations' : d['observations']
                           })

        data = json.dumps(chart_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiProjectsList(request):
    if request.method == 'GET':
        kwargs = {
        }
        projects_data = []
        projects_of_user = list(Project.objects.filter(created_by = request.user))
        final_data = {"data": []}
        for obj in projects_of_user:
           curSharingLevel = 'PRI'
           if obj.sharing_level == 'PRI':
                 curSharingLevel = dict(SHARINGLEVEL).get(obj.sharing_level) + '&nbsp<i class="fa fa-lock"></i>'
           else:
                 curSharingLevel = dict(SHARINGLEVEL).get(obj.sharing_level) + '&nbsp<i class="fa fa-unlock"></i>'
           projects_data.append({'id': obj.id,
                                  'title': obj.title_2,
                                  'user_note': obj.user_note,
                                  'type': dict(INVESTMENTBUILDING).get(obj.istheinvestmentinabuilding_12),
                                  'country': dict(COUNTRIES).get(obj.country_3),
                                  'date_updated':naturaltime(obj.date_updated),
                                  'sharing_level': curSharingLevel,
                                  })

           final_data = {"data":projects_data}
        data = json.dumps(final_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def ApiBenchmarkLoadProjects(request):
    if request.method == 'GET':
        kwargs = {
        }
        projects_data = []
        projects_of_user = list(Project.objects.filter(created_by = request.user))
        final_data = {"data": []}
        for obj in projects_of_user:

            projects_data.append({'id': obj.id,
                                  'title': obj.title_2,
                                  'type': dict(INVESTMENTBUILDING).get(obj.istheinvestmentinabuilding_12),
                                  'country': dict(COUNTRIES).get(obj.country_3),
                                  'selected': '',
                                  })
            final_data = {"data":projects_data}
        data = json.dumps(final_data, cls=DefaultEncoder)
        return HttpResponse(data)


@login_required
def ApiOverview(request):
    locale.setlocale(locale.LC_NUMERIC, '')
    if request.method == 'GET':
        kwargs = {
        }
        #Get count of all projects
        my_query = 'SELECT country_3,istheinvestmentinabuilding_12,CASE WHEN istheinvestmentinabuilding_12 = \'Building\' THEN count(id) ELSE 0 END COUNT_BUILDING,'+\
         'CASE WHEN istheinvestmentinabuilding_12 = \'Industry\' THEN count(id) ELSE 0 END COUNT_INDUSTRY,'+\
         'CASE WHEN istheinvestmentinabuilding_12 <> \'Industry\' AND istheinvestmentinabuilding_12 <> \'Building\' THEN count(id) ELSE 0 END COUNT_OTHER '+\
         'FROM public.derisk_app_project '+ \
         'WHERE "derisk_app_project"."sharing_level" = \'ANA\''+\
         'GROUP BY country_3,istheinvestmentinabuilding_12'
        cursor = connection.cursor()
        cursor.execute(my_query)
        raw_data = dictfetchall(cursor)

        #Get simple payback times,etc'
        my_query_payback = 'SELECT country_3,istheinvestmentinabuilding_12,'+\
         'CASE WHEN istheinvestmentinabuilding_12 = \'Building\' THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) ELSE 0 END PAYBACK_BUILDING,'+\
         'CASE WHEN istheinvestmentinabuilding_12 = \'Industry\' THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC)  ELSE 0 END PAYBACK_INDUSTRY,'+\
         'CASE WHEN istheinvestmentinabuilding_12 <> \'Industry\' AND istheinvestmentinabuilding_12 <> \'Building\'  THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_simple_payback_time_AA" ASC) ELSE 0 END PAYBACK_OTHER '+\
         'FROM public.derisk_app_project '+ \
         'WHERE "derisk_app_project"."sharing_level" = \'ANA\' AND "derisk_app_project"."indicator_simple_payback_time_AA" > 0'+\
         'GROUP BY country_3,istheinvestmentinabuilding_12'
        cursor = connection.cursor()
        cursor.execute(my_query_payback)
        raw_data_payback = dictfetchall(cursor)

        #Get Median Avoidance cost'
        my_query_avoidance = 'SELECT country_3,istheinvestmentinabuilding_12,'+\
         'CASE WHEN istheinvestmentinabuilding_12 = \'Building\' THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_avoidance_cost0" ASC) ELSE 0 END AVOIDANCE_BUILDING,'+\
         'CASE WHEN istheinvestmentinabuilding_12 = \'Industry\' THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_avoidance_cost0" ASC)  ELSE 0 END AVOIDANCE_INDUSTRY,'+\
         'CASE WHEN istheinvestmentinabuilding_12 <> \'Industry\' AND istheinvestmentinabuilding_12 <> \'Building\'  THEN PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "derisk_app_project"."indicator_avoidance_cost0" ASC) ELSE 0 END AVOIDANCE_OTHER '+\
         'FROM public.derisk_app_project '+ \
         'WHERE "derisk_app_project"."sharing_level" = \'ANA\' AND "derisk_app_project"."indicator_avoidance_cost0" > 0'+\
         'GROUP BY country_3,istheinvestmentinabuilding_12'
        cursor = connection.cursor()
        cursor.execute(my_query_avoidance)
        raw_data_avoidance = dictfetchall(cursor)

        #Get the list of all countries'
        my_query = 'SELECT country_3 '+\
         'FROM public.derisk_app_project '+ \
         'WHERE "derisk_app_project"."sharing_level" = \'ANA\''+\
         'GROUP BY country_3'
        cursor = connection.cursor()
        cursor.execute((my_query))
        country_data = dictfetchall(cursor)

        map_data =[]
        for curCountry in country_data:
            count_building = 0
            payback_building = 0
            avoidance_building = 0
            count_industry = 0
            payback_industry = 0
            avoidance_industry = 0
            count_other = 0
            payback_other = 0
            avoidance_other = 0
            for m in raw_data:
                if m['country_3'] == curCountry['country_3'] :
                    if m['istheinvestmentinabuilding_12'] == 'Building':
                        count_building = m['count_building']
                    elif m['istheinvestmentinabuilding_12'] == 'Industry':
                        count_industry = m['count_industry']
                    else:
                        count_other = m['count_other'] + count_other

            for m in raw_data_payback:
                if m['country_3'] == curCountry['country_3'] :
                    if m['istheinvestmentinabuilding_12'] == 'Building':
                        payback_building = m['payback_building']
                    elif m['istheinvestmentinabuilding_12'] == 'Industry':
                        payback_industry= m['payback_industry']
                    else:
                        payback_other= (m['payback_other'] + payback_other) / 2

            for m in raw_data_avoidance:
                if m['country_3'] == curCountry['country_3'] :
                    if m['istheinvestmentinabuilding_12'] == 'Building':
                        avoidance_building = m['avoidance_building']
                    elif m['istheinvestmentinabuilding_12'] == 'Industry':
                        avoidance_industry= m['avoidance_industry']
                    else:
                        avoidance_other= (m['avoidance_other'] + avoidance_other) / 2

            mycustomdata =''
            str_count_building='0'
            str_count_industry='0'
            str_count_other = '0'
            str_payback_building ='n.a'
            str_payback_industry = 'n.a'
            str_payback_other = 'n.a'
            str_avoidance_building ='n.a'
            str_avoidance_industry = 'n.a'
            str_avoidance_other = 'n.a'

            if count_building > 0:
                str_count_building = str(count_building)
            if count_industry > 0:
                str_count_industry = str(count_industry)
            if count_other > 0:
                str_count_other = str(count_other)
            if payback_building > 0:
                str_payback_building = '{0:n}'.format(round(payback_building,1))
            if payback_industry > 0:
                str_payback_industry = '{0:n}'.format(round(payback_industry, 1))
            if payback_other > 0:
                str_payback_other = '{0:n}'.format(round(payback_other, 1))
            if avoidance_building > 0:
                str_avoidance_building = '{0:n}'.format(round(avoidance_building,1))
            if avoidance_industry > 0:
                str_avoidance_industry = '{0:n}'.format(round(avoidance_industry, 1))
            if avoidance_other > 0:
                str_avoidance_other = '{0:n}'.format(round(avoidance_other, 1))

            #Infobox to appear in the chart
            mycustomdata = mycustomdata + '<i class=\'fa fa-building\'></i> <b>' + _('Building Projects') + '</b><br>Total:' + str_count_building
            mycustomdata = mycustomdata + '<br>' + _('Median Payback time') + ':' + str_payback_building
            mycustomdata = mycustomdata + '<br>' + _('Median Avoidance cost') + ':' + str_avoidance_building + '<br><br>'
            mycustomdata = mycustomdata + '<i class=\'fa fa-industry\'></i> <b>' + _('Industry Projects') + '</b><br>Total:' + str_count_industry
            mycustomdata = mycustomdata + '<br>' + _('Median Payback time') + ':' + str_payback_industry
            mycustomdata = mycustomdata + '<br>' + _('Median Avoidance cost') + ':' + str_avoidance_industry+ '<br><br>'
            #mycustomdata = mycustomdata + '<i class=\'fa fa-circle-0\'></i> <b>Other Projects</b><br>Total:' + str_count_other
            #mycustomdata = mycustomdata + '<br>Median Payback time:' + str_payback_other
            #mycustomdata = mycustomdata + '<br>Median Avoidance cost:' + str_avoidance_other + '<br>'

            map_data.append({'title': dict(COUNTRIES).get(curCountry['country_3']),
                           'id':curCountry['country_3'],
                           'color': '#34495E',
                           'customData': mycustomdata,
                           })

        data = json.dumps(map_data, cls=DefaultEncoder)
        return HttpResponse(data)

@login_required
def test(request):
    params = {}
    return render(request, 'test.html',params)

@login_required
def FactSheetQuick(request):
    params = {}
    factsheetselectorform = FactSheetSelectorForm()
    params['factsheetselectorform']= factsheetselectorform

    params['totalprojects'] = Project.objects.filter(sharing_level='ANA').count()

    #Number of projects buildings
    params['total_projects_buildings'] = Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Building').count()

    #Number of projects Industry
    params['total_projects_industry'] = Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Industry').count()

    # average payback time Buildings
    params['median_payback_buildings'] =round(Project.objects.filter(indicator_simple_payback_time_AA__gt=0,sharing_level='ANA',istheinvestmentinabuilding_12='Building').aggregate(median=Percentile('indicator_simple_payback_time_AA', 0.5, output_field=models.DecimalField()))['median'],1)

    # average payback time Industry
    params['median_payback_industry'] = round(Project.objects.filter(indicator_simple_payback_time_AA__gt=0, sharing_level='ANA',istheinvestmentinabuilding_12='Industry').aggregate(median=Percentile('indicator_simple_payback_time_AA', 0.5, output_field=models.DecimalField()))['median'], 1)

    # average avoidance cost Buildings
    params['median_avoidance_buildings'] = round(Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Building',indicator_avoidance_cost0__gt=0).aggregate(median=Percentile('indicator_avoidance_cost0', 0.5, output_field=models.DecimalField()))['median'], 1)

    #  average avoidance cost Industry
    params['median_avoidance_industry'] = round(Project.objects.filter(sharing_level='ANA',istheinvestmentinabuilding_12='Industry',indicator_avoidance_cost0__gt=0).aggregate(median=Percentile('indicator_avoidance_cost0', 0.5, output_field=models.DecimalField()))['median'], 1)

    return render(request, 'factsheet-quick.html',params)

@login_required
def FactSheetIndustry(request):
    params = {}
    totalprojects = Project.objects.filter(sharing_level='ANA').count()
    params['totalprojects'] = totalprojects
    factsheetselectorform = FactSheetSelectorForm()
    params['factsheetselectorform']= factsheetselectorform
    return render(request, 'factsheet-industry.html',params)

@login_required
def FactSheetBuildings(request):
    params = {}
    totalprojects = Project.objects.filter(sharing_level='ANA').count()
    params['totalprojects'] = totalprojects
    factsheetselectorform = FactSheetSelectorForm()
    params['factsheetselectorform']= factsheetselectorform
    return render(request, 'factsheet-buildings.html',params)


@login_required
def toolbox(request):
    params = {
        'aggregate_options': AGGREGATES,
        'filter_variables': FILTER_VARIABLES,
    }
    return render(request, 'toolbox/index.html', params)


@login_required
def toolbox(request, pk=''):
    params = {
        'aggregate_options': AGGREGATES,
        'filter_variables': FILTER_VARIABLES,
    }

    if pk:
        try:
            Chart.objects.filter(Q(created_by=request.user) | Q(is_template=True)).get(pk=pk)
        except Chart.DoesNotExist as e:
            return HttpResponse('Chart with id %s does not exist' % pk)

        params['auto_open'] = pk
    else:
        params['auto_create'] = True

    return render(request, 'toolbox/index.html', params)


@login_required
def toolbox_all(request):
    ctx = {
        'templates': Chart.objects.filter(is_template=True),
        'charts': Chart.objects.filter(created_by=request.user, is_template=False),
    }

    return render(request, 'toolbox/list-full.html', ctx)


@login_required
def Benchmark(request):
    params = {}
    totalprojects = Project.objects.filter(sharing_level='ANA').count()
    params['totalprojects'] = totalprojects
    benchmarkselectorform = BenchmarkSelectorForm()
    params['benchmarkselectorform']= benchmarkselectorform
    return render(request, 'benchmark.html',params)


# Chart-related views
# Note - These along with the Chart models & the toolbox templates could be moved to a seperate app in the future

@login_required
def list_charts(request):
    # ensure GET request
    if request.method != 'GET':
        return HttpResponse('Only `GET` method allowed', status=400)

    ctx = {
        'charts': Chart.objects.filter(created_by=request.user, is_template=False),
    }

    return render(request, 'toolbox/chart-table.html', ctx)


@login_required
def save_chart(request):
    # ensure POST request
    if request.method != 'POST':
        return HttpResponse('Only `POST` method allowed', status=400)

    # get the chart to update (or new chart)
    chart_id = request.POST.get('chart_id', '')
    chart_title = request.POST.get('title', '')
    chart_fields = request.POST.get('chart_options', '')
    chart_filters = request.POST.get('chart_filters', '')
    chart_type = request.POST.get('chart_type', '')
    chart_format = request.POST.get('chart_format', '')

    if chart_id:  # existing chart
        try:
            chart = Chart.objects.filter(Q(created_by=request.user) | Q(is_template=True)).get(pk=chart_id)
        except Chart.DoesNotExist as e:
            return HttpResponse('Chart not found', status=404)
    else:  # new chart
        # we need all the info in this case
        if not chart_title or not chart_fields:
            return HttpResponse('`title` and `fields` are both required for a new chart', status=400)

        chart = Chart(created_by=request.user)

    # update the provided fields
    if chart_title:
        chart.title = chart_title

    if chart_fields:
        # ensure json
        chart.fields = json.dumps(json.loads(chart_fields))

    if chart_type:
        chart.chart_type = chart_type

    if chart_format:
        chart.chart_format = chart_format

    if chart_filters:
        chart.filters = chart_filters

    # make sure to clone chart for templates
    if chart.is_template and not request.user.is_superuser:
        # change owner, mark as plain chart & save as new object
        chart.created_by = request.user
        chart.is_template = False
        chart.pk = None

    # save the chart
    chart.save()

    # send the ID
    return HttpResponse(chart.pk)


@login_required
def delete_chart(request, pk):
    # ensure POST request
    if request.method != 'POST':
        return HttpResponse('Only `POST` method allowed', status=400)

    try:
        chart = Chart.objects.get(pk=pk, created_by=request.user)
    except Chart.DoesNotExist as e:
        return HttpResponse('Chart not found', status=404)

    # delete & send OK response
    chart.delete()
    return HttpResponse('', status=204)


@login_required
def open_chart(request, pk):
    # ensure GET request
    if request.method != 'GET':
        return HttpResponse('Only `GET` method allowed', status=400)

    # check if chart exists & is owned by this user
    try:
        chart = Chart.objects.filter(Q(created_by=request.user) | Q(is_template=True)).get(pk=pk)
    except Chart.DoesNotExist as e:
        return HttpResponse('Chart not found', status=404)

    # return the chart info
    return JsonResponse({
        'title': chart.title,
        'chartType': chart.chart_type,
        'chartFormat': chart.chart_format,
        'chartOptions': json.loads(chart.fields),
        'chartFilters': chart.filters,
        'chartPolicy': get_field_policy(user=request.user,
                                        chart_type=chart.chart_type, chart_format=chart.chart_format),
    }, safe=True, encoder=DefaultEncoder)


def filter_info(request):
    variable = request.GET.get('variable', '')
    if not variable:
        return HttpResponse('`variable` field required', status=400)

    # replace FK variable
    if variable == 'nonfinancialbenefits_67':
        variable = 'nonfinancialbenefits_67__description'

    # nested lookup variable logic
    model = Project
    from_related = False

    parts = variable.split('__')

    # no more than one-step join available right now
    if len(parts) > 2:
        return HttpResponse('Nested lookups are not supported', status=501)

    # iterate variable parts
    for part in parts:
        # find the field & its type
        pFields = model._meta.get_fields()
        for pField in pFields:
            if pField.name != part:
                continue

            if type(pField) == ManyToManyField:
                model = pField.related_model
                from_related = True
            elif type(pField) == CharField:
                options = []

                if not options:
                    options = [{'name': 'No value', 'value': ''}]
                    if from_related:
                        for v in model.objects.order_by().values_list('id', part).distinct():
                            if v:
                                options.append({'name': v[1], 'value': v[0]})
                    else:
                        for v in model.objects.order_by().values_list(variable, flat=True).distinct():
                            if v:
                                options.append({'name': v, 'value': v})
                else:
                    for c in pField.choices:
                        options.append({'name': c[1], 'value': c[0]})

                return JsonResponse({'type': 'select', 'options': options})
            else:
                return JsonResponse({'type': 'number'})

