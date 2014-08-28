from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q, Count
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django_tables2 import RequestConfig
from forms import DataExportForm
from libraryuse.tables import PersonTypeTable, DepartmentTable, DivisionTable, ProgramTable
from models import LibraryVisit
import csv
import json
import time

@login_required
def index(request):
    context = {}
    return render_to_response('libraryuse/dashboard.html', context)

@login_required
def reports_index(request):
    context = {}
    return redirect('/#/reports')

@login_required
def export(request):
    context = RequestContext(request, {})
    export_form = None
    if request.method == 'POST':
        export_form = DataExportForm(request.POST)
        #i suspect because the dates are not actaully coming through
        if export_form.is_valid():
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="libraryuse.csv"'
            writer = csv.writer(response)

            start_date = export_form.cleaned_data['start_date']
            end_date = export_form.cleaned_data['end_date']
            print(start_date)
            visits = LibraryVisit.objects.filter(visit_time__range=[start_date, end_date])

            writer.writerow(['visit_time', 'term_number', 'location', 'prsn_c_type', \
                             'prsn_e_type', 'emjo_c_clsf', 'dprt_c', \
                             'edprt_n', 'dvsn_i', 'dvsn_n', \
                             'empe_c_fclt_rank', 'prsn_c_type_hc', \
                             'prsn_e_type_hc', 'emjo8hc_c_clsf', 'dprt8hc_c', \
                             'dprt8hc_n', 'dvsn8hc_i', 'dvsn8hc_n', \
                             'acca_i', 'acpr_n', 'acpl_n',  \
                             'stdn_e_clas', 'stdn_f_ungr', 'stdn_f_cmps_on'])
            for v in visits:
                writer.writerow([v.visit_time, v.term_number, v.location, \
                                v.prsn_c_type, v.prsn_e_type, v.emjo_c_clsf, \
                                v.dprt_c, v.dprt_n, v.dvsn_i, v.dvsn_n, \
                                v.empe_c_fclt_rank, v.prsn_c_type_hc, \
                                v.prsn_e_type_hc, v.emjo8hc_c_clsf, v.dprt8hc_c, \
                                v.dprt8hc_n, v.dvsn8hc_i, v.dvsn8hc_n, v.acca_i, \
                                v.acpr_n, v.acpl_n, v.stdn_e_clas, v.stdn_f_ungr, \
                                v.stdn_f_cmps_on])

            return response

    else:
        export_form = DataExportForm()

    return render(request, 'libraryuse/export.html', {'form': export_form,})


@login_required
def summary(request):

    pt_t = PersonTypeTable(_usage('person_type'))
    RequestConfig(request).configure(pt_t)

    dpt_t = DepartmentTable(_usage('department'))
    RequestConfig(request).configure(dpt_t)

    div_t = DivisionTable(_usage('division'))
    RequestConfig(request).configure(div_t)

    pgm_t = ProgramTable(_usage('program'))
    RequestConfig(request).configure(pgm_t)

    pln_t = ProgramTable(_usage('plan'))
    RequestConfig(request).configure(pln_t)

    cls_t = ProgramTable(_usage('class'))
    RequestConfig(request).configure(cls_t)

    context = {'person_type': pt_t,
               'department': dpt_t,
               'division': div_t,
               'program': pgm_t,
               'plan': pln_t,
               'class': cls_t,
               }
    return render(request, 'libraryuse/summary.html', context)

def chart_data(numbers, distinct_flag):

    data = []
    visits = []
    data.append('jsonResponse({"data":[')

    if distinct_flag is False:
        for number in numbers:
            if number.has_key('visit_time'):
                dt = datetime.strptime(str(number['visit_time']), '%Y-%m-%d %H:%M:%S')
                epoch = int(time.mktime(dt.timetuple()))
                # We have to add the three zeros to work with HighCharts
                visits.append('[%s000,%s]' % (epoch, number['total']))
            elif number.has_key('acpl_n'):
                acpl_n = number['acpl_n']
                visits.append('["%s",%s]' % (acpl_n, number['total']))
            elif number.has_key('dprt_n'):
                dprt_n = number['dprt_n']
                visits.append('["%s",%s]' % (dprt_n, number['total']))
            elif number.has_key('dvsn_n'):
                dvsn_n = number['dvsn_n']
                visits.append('["%s",%s]' % (dvsn_n, number['total']))
        data.append(', '.join(visits))
    else:
        data.append(numbers)
    data.append('],"queried_at":["%s"]})' % datetime.now())

    return(data)

def location_name(library):
    if 'woodruff' in library:
        return('LOCATION: WL TURNSTILE (1&2)')
    elif 'law' in library:
        return('LOCATION: LAW ACCESS')
    elif 'health' in library:
        return('LOCATION: HEALTH SCIENCES LIBRARY')
    else:
        return(None)

#@login_required

def total_usage(request, library, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    if distinct_flag == False:
        numbers = LibraryVisit.objects.values('visit_time') \
                    .annotate(total=Count('visit_time')) \
                    .order_by('visit_time') \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location)
        print(numbers.query)
    else:
        numbers = LibraryVisit.objects \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def on_off_campus(request, library, resident, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    if distinct_flag == False:
        numbers = LibraryVisit.objects.values('visit_time') \
                    .annotate(total=Count('visit_time')) \
                    .order_by('visit_time') \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_f_cmps_on = resident) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))
    else:
        numbers = LibraryVisit.objects \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_f_cmps_on = resident) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E')) \
                    .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def student_class(request, library, classification, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    if distinct_flag == False:
        numbers = LibraryVisit.objects.values('visit_time') \
                    .annotate(total=Count('visit_time')) \
                    .order_by('visit_time') \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_e_clas = classification) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))
    else:
        numbers = LibraryVisit.objects \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_e_clas = classification) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E')) \
                    .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def faculty_staff_class(request, library, classification, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    if distinct_flag == False:
        numbers = LibraryVisit.objects.values('visit_time') \
                    .annotate(total=Count('visit_time')) \
                    .order_by('visit_time') \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(Q(prsn_c_type = 'F')) \
                    .filter(dvsn_n = classification)
    else:
        numbers = LibraryVisit.objects \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(Q(prsn_c_type = 'F')) \
                    .filter(dvsn_n = classification) \
                    .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def top_academic_plan(request, library, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    numbers = LibraryVisit.objects.values('acpl_n') \
                .annotate(total=Count('acpl_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def top_dprtn(request, library, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def top_devision(request, library, start, end):

    distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    data = chart_data(numbers, distinct_flag)

    return StreamingHttpResponse(data, content_type='application/json')

def calculate_dates(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()
    date_delta = end_date - start_date
    weeks = date_delta.days/7
    data = {}
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['weeks'] = weeks

    return data

def int_day(dow):
    # This translates the MySQL days to dateutil days
    # In Django MySQL Monday = 2 but 0 in dateutil
    if dow == 1:
        return 6
    elif dow == 2:
        return 0
    elif dow == 3:
        return 1
    elif dow == 4:
        return 2
    elif dow == 5:
        return 3
    elif dow == 6:
        return 4
    elif dow == 7:
        return 5

def averages(request, library, start, end, start_hour, end_hour, dow):

    dates = calculate_dates(start, end)

    location = location_name(library)

    count = 0
    totals = 0

    while (count <= dates['weeks']):
        start_time = dates['start_date']+relativedelta(weeks=+count, hour=int(start_hour), weekday=int_day(dow))
        end_time = dates['start_date']+relativedelta(weeks=+count, hour=int(end_hour), weekday=int_day(dow))
        numbers = LibraryVisit.objects \
            .values('visit_time') \
            .annotate(total=Count('visit_time')) \
            .filter(visit_time__range=[start_time, end_time])\
            .filter(visit_time__week_day = dow) \
            .filter(location = location)
        print(numbers)
        for number in numbers:
            if number['visit_time'].hour != end_hour:
                totals += number['total']
        count += 1

    average = totals / count

    jsonp = 'jsonResponse({'
    jsonp += '"start_date":"%s",' % start
    jsonp += '"end_date":"%s",' % end
    jsonp += '"start_hour":"%s",' % start_hour
    jsonp += '"end_hour":"%s",' % end_hour
    jsonp += '"dow":"%s",' % dow
    jsonp += '"average":"%s"' % average
    jsonp += '})'

    return StreamingHttpResponse(jsonp, content_type='application/json')

def classifications(request):
    student_classes = LibraryVisit.objects.values_list('stdn_e_clas', flat=True).distinct().exclude(stdn_e_clas__isnull=True)
    academic_plans = LibraryVisit.objects.values_list('acpl_n', flat=True).distinct().exclude(acpl_n__isnull=True)
    departments = LibraryVisit.objects.values_list('dprt_n', flat=True).distinct().exclude(dprt_n__isnull=True)
    academic_career = LibraryVisit.objects.values_list('acca_i', flat=True).distinct().exclude(acca_i__isnull=True).filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))
    faculty_divisions = LibraryVisit.objects.values_list('dvsn_n', flat=True).distinct().exclude(dvsn_n__isnull=True).filter(Q(prsn_c_type = 'F'))

    jsonp = 'jsonCategories({'

    jsonp += '"student_classes":["'
    jsonp += '","'.join(student_classes)
    jsonp += '"],'

    jsonp += '"academic_plans":["'
    jsonp += '","'.join(academic_plans)
    jsonp += '"],'

    jsonp += '"academic_career":["'
    jsonp += '","'.join(academic_career)
    jsonp += '"],'

    jsonp += '"faculty_divisions":["'
    jsonp += '","'.join(faculty_divisions)
    jsonp += '"]',

    jsonp += '"departments":["'
    jsonp += '","'.join(departments)
    jsonp += '"]'

    jsonp += '})'

    return StreamingHttpResponse(jsonp, content_type='application/json')

def student_classifications(request):
    student_classes = LibraryVisit.objects.values_list('stdn_e_clas', flat=True).distinct().exclude(stdn_e_clas__isnull=True)
    acidemic_plans = LibraryVisit.objects.values_list('acpl_n', flat=True).distinct().exclude(stdn_e_clas__isnull=True)
    department = LibraryVisit.objects.values_list('dprt_n', flat=True).distinct().exclude(stdn_e_clas__isnull=True)

    data = []
    jsonp = []

    def add_classes(classes, title):
        title_list = [title]
        class_list = []

        for item in classes:
            class_list.append(str('%s' % item))

        list.append(class_list)
        return title_list

    data.append(add_classes(student_classes, 'student_classes'))
    data.append(add_classes(acidemic_plans, 'acidemic_plans'))
    data.append(add_classes(department, 'department'))
    jsonp.append(json.dumps(data))

    return HttpResponse(jsonp, content_type='application/json')
