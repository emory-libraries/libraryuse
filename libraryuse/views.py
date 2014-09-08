from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import json
from django.db.models import Q, Count
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
from forms import DataExportForm
from models import LibraryVisit
import time

@login_required
def index(request):
    context = {}
    return render_to_response('libraryuse/dashboard.html', context)

@login_required
def reports_index(request):
    context = {}
    return redirect('/#/reports')

def chart_data(numbers, distinct, start, end, library,**keyword_parameters):

    data = []
    visits = []
    title = ""
    data.append('{"data":[')


    for number in numbers:
        if number.has_key('visit_time'):
            dt = datetime.strptime(str(number['visit_time']), '%Y-%m-%d %H:%M:%S')
            epoch = int(time.mktime(dt.timetuple()))
            # We have to add the three zeros to work with HighCharts
            visits.append('[%s000,%s]' % (epoch, number['total']))
        elif number.has_key('acpl_n'):
            title = "Academic Plan"
            acpl_n = number['acpl_n']
            visits.append('{"label":"%s","value":%s}' % (acpl_n, number['total']))
        elif number.has_key('dprt_n'):
            title = "Department"
            dprt_n = number['dprt_n']
            visits.append('{"label":"%s","value":%s}' % (dprt_n, number['total']))
        elif number.has_key('dvsn_n'):
            title = "Faculty Division"
            dvsn_n = number['dvsn_n']
            visits.append('{"label":"%s","value":%s}' % (dvsn_n, number['total']))
    data.append(', '.join(visits))

    data.append('],')
    
    if('sum' in keyword_parameters):
        data.append('"total_sum":%s,' % keyword_parameters['sum'])
    
    
    data.append('"meta":{')
    data.append('"strt_date":["%s"],' % start)
    data.append('"end_date":["%s"],' % end)
    data.append('"library":["%s"],' % library)
    data.append('"title":["%s"]' % title)
    data.append('},')

    data.append('"distinct":["%s"],"queried_at":["%s"]}' % (distinct, datetime.now()))

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

def get_classifications(filter_by):

    if filter_by == 'stdn_e_clas':
        return LibraryVisit.objects \
            .values_list('stdn_e_clas', flat=True) \
            .distinct() \
            .exclude(stdn_e_clas__isnull=True) \
            .order_by('stdn_e_clas')

    elif filter_by == 'acpl_n':
        return LibraryVisit.objects \
            .values_list('acpl_n', flat=True) \
            .distinct() \
            .exclude(acpl_n__isnull=True) \
            .order_by('acpl_n')

    elif filter_by == 'dprt_n':
        return LibraryVisit.objects \
            .values_list('dprt_n', flat=True) \
            .distinct() \
            .exclude(dprt_n__isnull=True) \
            .order_by('dprt_n')

    elif filter_by == 'acca_i':
        return LibraryVisit.objects \
            .values_list('acca_i', flat=True) \
            .distinct().exclude(acca_i__isnull=True) \
            .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E')) \
            .order_by('acca_i')

    elif filter_by == 'dvsn_n':
        return LibraryVisit.objects \
            .values_list('dvsn_n', flat=True) \
            .distinct() \
            .exclude(dvsn_n__isnull=True) \
            .filter(Q(prsn_c_type = 'F')) \
            .order_by('dvsn_n')

#@login_required

def total_usage(request, library, start, end):

    #distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    numbers = LibraryVisit.objects.values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .order_by('visit_time') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    distinct = LibraryVisit.objects \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def on_off_campus(request, library, resident, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .order_by('visit_time') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(stdn_f_cmps_on = resident) \
                .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))

    distinct = LibraryVisit.objects \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(stdn_f_cmps_on = resident) \
                .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E')) \
                .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def student_class(request, library, classification, start, end):

    #distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    numbers = LibraryVisit.objects.values('visit_time') \
                    .annotate(total=Count('visit_time')) \
                    .order_by('visit_time') \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_e_clas = classification) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))

    distinct = LibraryVisit.objects \
                    .filter(visit_time__range=[start, end]) \
                    .filter(location = location) \
                    .filter(stdn_e_clas = classification) \
                    .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E')) \
                    .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def faculty_staff_class(request, library, classification, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .order_by('visit_time') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(Q(prsn_c_type = 'F')) \
                .filter(dvsn_n = classification)

    distinct = LibraryVisit.objects \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(Q(prsn_c_type = 'F')) \
                .filter(dvsn_n = classification) \
                .values("prsn_i_ecn").distinct().count()

    data = chart_data(numbers, distinct, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def top_academic_plan(request, library, start, end):

    distinct = None

    location = location_name(library)

    numbers = LibraryVisit.objects.values('acpl_n') \
                .annotate(total=Count('acpl_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))
    
    sum = numbers.values('acpl_n').count()
    
    data = chart_data(numbers, distinct, start, end, library, sum=sum)

    return StreamingHttpResponse(data, content_type='application/json')

def top_dprtn(request, library, start, end):

    distinct = None

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)
    
    sum = numbers.values('dprt_n').count()

    data = chart_data(numbers, distinct, start, end, library, sum=sum)

    return StreamingHttpResponse(data, content_type='application/json')

def top_division(request, library, start, end):

    distinct = None

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)
                
    sum = numbers.values('dvsn_n').count()

    data = chart_data(numbers, distinct, start, end, library, sum=sum)

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
    # This translates the MySQL days to dateutil days.
    # In Django MySQL Monday = 2 but 0 in dateutil.
    dow_ints = {
        1 : 6,
        2 : 0,
        3 : 1,
        4 : 2,
        5 : 3,
        6 : 4,
        7 : 5
    }

    return int(dow_ints[dow])

def alph_day(dow):
    # This translates the MySQL days to dateutil days.
    # In Django MySQL Monday = 2 but 0 in dateutil.
    dow_alphs = {
        '1' : 'Sunday',
        '2' : 'Monday',
        '3' : 'Tuesday',
        '4' : 'Wednesday',
        '5' : 'Thursday',
        '6' : 'Friday',
        '7' : 'Saturday'
    }

    return dow_alphs[dow]

def total_averages(request, library, start, end, start_hour, end_hour, dow):

    dates = calculate_dates(start, end)

    location = location_name(library)

    count = 0
    totals = 0

    while (count <= dates['weeks']):
        start_time = dates['start_date']+relativedelta(weeks=+count, hour=int(start_hour), weekday=int_day(int(dow)))
        end_time = dates['start_date']+relativedelta(weeks=+count, hour=int(end_hour), weekday=int_day(int(dow)))
        numbers = LibraryVisit.objects \
            .values('visit_time') \
            .annotate(total=Count('visit_time')) \
            .filter(visit_time__range=[start_time, end_time])\
            .filter(visit_time__week_day = dow) \
            .filter(location = location)
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

def averages(request, library, start, end, start_hour, end_hour, dow, filter_on):
    dates = calculate_dates(start, end)

    location = location_name(library)

    count = 0
    totals = 0

    classifications = get_classifications(filter_on)

    jsonp = '{"data":{'
    counts = []

    for classification in classifications:

        while (count <= dates['weeks']):
            start_time = dates['start_date']+relativedelta(weeks=+count, hour=int(start_hour), weekday=int_day(int(dow)))
            end_time = dates['start_date']+relativedelta(weeks=+count, hour=int(end_hour), weekday=int_day(int(dow)))
            numbers = LibraryVisit.objects \
                .values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .filter(visit_time__range=[start_time, end_time])\
                .filter(visit_time__week_day = dow) \
                .filter(location = location) \
                .filter(**{ filter_on: classification })
            for number in numbers:
                if number['visit_time'].hour != end_hour:
                    totals += number['total']
            count += 1

        average = totals / count
        counts.append('"%s":{"label":"%s","value":%s}' % (slugify(classification), classification, average))
        count = 0
        totals = 0

    jsonp += ', '.join(counts)
    jsonp += '},'
    jsonp += '"meta":{'
    jsonp += '"strt_date":["%s"],' % start
    jsonp += '"end_date":["%s"],' % end
    jsonp += '"strt_hour":["%s"],' % start_hour
    jsonp += '"end_hour":["%s"],' % end_hour
    jsonp += '"dow":["%s"],' % alph_day(dow)
    jsonp += '"queried_at":["%s"]' % datetime.now()
    jsonp += '}}'

    return StreamingHttpResponse(jsonp, content_type='application/json')

def percent_date(whole, part, label):
    return '[%s: %s]' % (label, (100 * float(part)/float(whole)))

def percentage(request, library, start, end, filter_on):
    '''
    get total based on filter then iterate
    '''

def classifications(request):

    student_classes = get_classifications('stdn_e_clas')

    academic_plans = get_classifications('acpl_n')

    departments = get_classifications('dprt_n')

    academic_career = get_classifications('acca_i')

    faculty_divisions = get_classifications('dvsn_n')

    jsonp = '{'

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
    jsonp += '"],'

    jsonp += '"departments":["'
    jsonp += '","'.join(departments)
    jsonp += '"]'

    jsonp += '}'

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
