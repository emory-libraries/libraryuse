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

def chart_data(numbers, distinct, total, start, end, library):

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
        elif number.has_key('acca_i'):
            title = "Academic Career"
            acca_i = number['acca_i']
            visits.append('{"label":"%s","value":%s}' % (acca_i, number['total']))
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

    data.append('"meta":{')
    data.append('"strt_date":["%s"],' % start)
    data.append('"end_date":["%s"],' % end)
    data.append('"library":["%s"],' % library)
    data.append('"title":["%s"]' % title)
    data.append('},')

    data.append('"distinct":["%s"],' % distinct)
    data.append('"total":["%s"],' % total)
    data.append('"queried_at":["%s"]}' % datetime.now())

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
            .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S')) \
            .order_by('acca_i') 

    elif filter_by == 'dvsn_n':
        return LibraryVisit.objects \
            .values_list('dvsn_n', flat=True) \
            .distinct() \
            .exclude(dvsn_n__isnull=True) \
            .filter(Q(prsn_c_type = 'F')) \
            .order_by('dvsn_n')

    else:
        return LibraryVisit.objects \
            .values_list('dprt_n', flat=True) \
            .distinct() \
            .exclude(dprt_n__isnull=True) \
            .order_by('dprt_n') \
            .filter(dvsn_n = filter_by)

#@login_required

def total_usage(request, library, person_type, start, end):

    #distinct_flag = request.GET.get('distinct', False)

    location = location_name(library)

    total_count = LibraryVisit.objects.values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .order_by('visit_time') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    if person_type == 'all':
        numbers = total_count

    elif person_type == 'student':
        numbers = total_count.filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S'))

    elif person_type == 'faculty':
        numbers = total_count.filter(prsn_c_type = 'F')

    elif person_type == 'staff':
        numbers = total_count.filter(prsn_c_type = 'E')

    distinct = numbers.values("prsn_i_ecn").distinct().count()

    total = numbers.values("prsn_i_ecn").count()

    data = chart_data(numbers, distinct, total, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def on_off_campus(request, library, resident, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('visit_time') \
                .annotate(total=Count('visit_time')) \
                .order_by('visit_time') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(stdn_f_cmps_on = resident) \
                .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S'))

    distinct = numbers.values("prsn_i_ecn").distinct().count()

    total = numbers.values("prsn_i_ecn").count()

    data = chart_data(numbers, distinct, total, start, end, library)

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
                .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S'))

    distinct = numbers.values("prsn_i_ecn").distinct().count()

    total = numbers.values("prsn_i_ecn").count()

    data = chart_data(numbers, distinct, total, start, end, library)

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

    distinct = numbers.values("prsn_i_ecn").distinct().count()

    total = numbers.values("prsn_i_ecn").count()

    data = chart_data(numbers, distinct, total, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def top_academic_plan(request, library, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('acpl_n') \
                .annotate(total=Count('acpl_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S'))

    distinct = numbers.values('acpl_n').distinct().count()

    total = numbers.values('acpl_n').count()

    data = chart_data(numbers, distinct, total, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

# def top_academic_career(request, library, start, end):
# 
#     location = location_name(library)
# 
#     numbers = LibraryVisit.objects.values('acca_i') \
#                 .annotate(total=Count('acca_i')) \
#                 .order_by('-total') \
#                 .filter(visit_time__range=[start, end]) \
#                 .filter(location = location) \
#                 .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S'))
# 
#     distinct = numbers.values('acca_i').distinct().count()
# 
#     total = numbers.values('acca_i').count()
# 
#     data = chart_data(numbers, distinct, total, start, end, library)
# 
#     return StreamingHttpResponse(data, content_type='application/json')


def top_dprtn(request, library, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    distinct = numbers.values('dprt_n').distinct().count()

    total = numbers.values('dprt_n').count()

    data = chart_data(numbers, distinct, total, start, end, library)

    return StreamingHttpResponse(data, content_type='application/json')

def top_division(request, library, start, end):

    location = location_name(library)

    numbers = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .order_by('-total') \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location)

    distinct = numbers.values('dvsn_n').distinct().count()

    total = numbers.values('dvsn_n').count()

    data = chart_data(numbers, distinct, total, start, end, library)

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

    jsonp = '{'
    jsonp += '"start_date":"%s",' % start
    jsonp += '"end_date":"%s",' % end
    jsonp += '"start_hour":"%s",' % start_hour
    jsonp += '"end_hour":"%s",' % end_hour
    jsonp += '"dow":"%s",' % dow
    jsonp += '"data":{"average":"%s"}' % average
    jsonp += '}'

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

def faculty_dprt_count(request, library, start, end):

    '''
    {
        "data": {
            "divs": {
                "division-name-slug": {
                    "label": "Division Name",
                    "value": 10009,
                    "depts": {
                        "department-name-slug": {
                            "label": "Department Name",
                            "value": 9990
                        }
                    }
                }
            }
        },
        "meta":{
            "start_date": "YYYY-MM-DD",
            "end_date":  "YYYY-MM-DD",
            "library": "library name",
            "title": "Faculty Department"
        }
    }
    '''

    def division_count(division, location, start, end):
        count = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(dvsn_n = division)

        if count:
            return count[0]['total']
        else:
            return 0

    def department_count(department, location, start, end):
        count = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(dprt_n = department)

        if count:
            return count[0]['total']
        else:
            return 0

    location = location_name(library)

    faculty_divisions = get_classifications('dvsn_n')

    jsonp = '{"data":{"divs":{'
    jsonp += '"'

    faculty_divisions_list = (sorted(faculty_divisions.reverse()[1:]))


    for faculty_division in faculty_divisions_list:

        visit_count = division_count(faculty_division, location, start, end)
        departments = get_classifications(faculty_division)
        departments_list = (sorted(departments.reverse()[1:]))
        last_departments = departments.reverse()[:1]

        jsonp += '%s": {' % slugify(faculty_division)

        jsonp += '"label": "%s",' % faculty_division

        jsonp += '"value": "%s",' % visit_count

        jsonp += '"depts":{'

        for department in departments_list:

            department_visit_count = department_count(department, location, start, end)

            jsonp += '"%s":{' % slugify(department)

            jsonp += '"label": "%s",' % department

            jsonp += '"value": "%s"' % department_visit_count

            jsonp += '},'

        for last_department in last_departments:

            last_department_visit_count = department_count(last_department, location, start, end)

            jsonp += '"%s":{' % slugify(last_department)

            jsonp += '"label": "%s",' % last_department

            jsonp += '"value": "%s"' % last_department_visit_count

            jsonp += '}'

        jsonp += '}'

        jsonp += '},"'

    last_faculty_divisions = faculty_divisions.reverse()[:1]

    for last_faculty_division in last_faculty_divisions:

        last_division_count = division_count(last_faculty_division, location, start, end)
        last_departments = get_classifications(last_faculty_division)
        last_departments_list = sorted(last_departments.reverse()[1:])
        final_departments = last_departments.reverse()[:1]

        jsonp += '%s":{' % slugify(last_faculty_division)
        jsonp += '"label": "%s",' % last_faculty_division
        jsonp += '"value": "%s",' % last_division_count
        jsonp += '"depts":{'

        for final_department in last_departments_list:

            final_department_visit_count = department_count(final_department, location, start, end)

            jsonp += '"%s": {' % slugify(final_department)

            jsonp += '"label": "%s",' % final_department

            jsonp += '"value": "%s"' % final_department_visit_count

            jsonp += '},'

        for last_final_department in final_departments:

            last_final_department_visit_count = department_count(last_final_department, location, start, end)

            jsonp += '"%s": {' % slugify(last_final_department)

            jsonp += '"label": "%s",' % last_final_department

            jsonp += '"value": "%s"' % last_final_department_visit_count

            jsonp += '}'

        jsonp += '}'
        jsonp += '}}}'

    jsonp += ',"meta":{'

    jsonp += '"library":["%s"],' % library

    jsonp += '"strt_date":["%s"],' % start

    jsonp += '"end_date":["%s"],' % end

    jsonp += '"title":["%s"]' % "Faculty Department"

    jsonp += '}'

    jsonp += ',"queried_at": "%s"' % datetime.now()

    jsonp += '}'

    return StreamingHttpResponse(jsonp, content_type='application/json')

def faculty_divs_dprt(request, library, start, end):

    '''
    {
        "data": {
            "divs": [
                {
                  "label": "Division Name",
                  "value": 10009,
                  "depts": [
                      [
                        "label": "Department Name",
                        "value": 9990
                      ]
                  ]
                }
            ]
        },
        "meta":{
            "start_date": "YYYY-MM-DD",
            "end_date":  "YYYY-MM-DD",
            "library": "library name",
            "title": "Faculty Department"
        }
    }
    '''
    def division_totals(location, start, end):
        count = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .order_by('-total')

        if count:
            return count
        else:
            return 0
            
    def division_count(division, location, start, end):
        count = LibraryVisit.objects.values('dvsn_n') \
                .annotate(total=Count('dvsn_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(dvsn_n = division)

        if count:
            return count[0]['total']
        else:
            return 0


    def department_totals(location, start, end):
        count = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .order_by('-total')

        if count:
            return count
        else:
            return 0
            
    def department_count(department, location, start, end):
        count = LibraryVisit.objects.values('dprt_n') \
                .annotate(total=Count('dprt_n')) \
                .filter(visit_time__range=[start, end]) \
                .filter(location = location) \
                .filter(dprt_n = department)

        if count:
            return count[0]['total']
        else:
            return 0

    location = location_name(library)

    faculty_divisions = get_classifications('dvsn_n')

    jsonp = '{"data":{"divs":['
    
    faculty_divisions_list = division_totals(location, start, end)

    for faculty_division in faculty_divisions_list:
        
        faculty_division_name = faculty_division["dvsn_n"]

        visit_count = faculty_division["total"]

        departments = get_classifications(faculty_division_name)
        departments_list = department_totals(location, start, end)
        last_departments = departments.reverse()[:1]

        jsonp += '{'

        jsonp += '"label": "%s",' % faculty_division_name

        jsonp += '"value": "%s",' % visit_count

        jsonp += '"depts":['

        for department in departments_list:
            
            department_name = department["dprt_n"]

            department_visit_count = department["total"]
            
            jsonp += '{'

            jsonp += '"label": "%s",' % department_name

            jsonp += '"value": "%s"' % department_visit_count

            jsonp += '},'

        for last_department in last_departments:
            #remove last comma
            if(jsonp[-1:] != '['):
              jsonp = jsonp[:-1]

        jsonp += ']},'

    last_faculty_divisions = faculty_divisions.reverse()[:1]

    for last_faculty_division in last_faculty_divisions:
        #remove last comma
        if(jsonp[-1:] != '['):
          jsonp = jsonp[:-1]

        jsonp += ']'
        jsonp += '}'

    jsonp += ',"meta":{'

    jsonp += '"library":["%s"],' % library

    jsonp += '"strt_date":["%s"],' % start

    jsonp += '"end_date":["%s"],' % end

    jsonp += '"title":["%s"]' % "Faculty Department"

    jsonp += '}'

    jsonp += ',"queried_at": "%s"' % datetime.now()

    jsonp += '}'

    return StreamingHttpResponse(jsonp, content_type='application/json')


def top_academic_career(request, library, start, end):

    '''
    {
      "data": [
                {
                  "label": "School Name",
                  "value": 10009,
                  "data": [
                      [
                        epoch_timestamp,
                        value
                      ]
                  ]
                }
        ],
        "meta":{
            "start_date": "YYYY-MM-DD",
            "end_date":  "YYYY-MM-DD",
            "library": "library name",
            "title": "Academic Career"
        }
    }
    '''
    
    
    def career_list(location, start, end):
        record = LibraryVisit.objects \
            .values('acca_i') \
            .filter(visit_time__range=[start, end]) \
            .filter(location = location) \
            .filter(Q(prsn_c_type = 'B') | Q(prsn_c_type = 'S')) \
            .annotate(total=Count('acca_i')) \
            .order_by('-total')

        return record

    location = location_name(library)

    academic_careers = career_list(location, start, end)

    jsonp = '{"data":['

    academic_careers_list = academic_careers

    for academic_career in academic_careers_list:
      
      academic_career_name = academic_career["acca_i"]
      
      visits =[]
      
      visit_count = academic_career["total"]
    
      numbers = LibraryVisit.objects.values('visit_time') \
                  .annotate(total=Count('visit_time')) \
                  .order_by('visit_time') \
                  .filter(visit_time__range=[start, end]) \
                  .filter(location = location) \
                  .filter(acca_i = academic_career_name)
                  
      for number in numbers:
          if number.has_key('visit_time'):
              dt = datetime.strptime(str(number['visit_time']), '%Y-%m-%d %H:%M:%S')
              epoch = int(time.mktime(dt.timetuple()))
              # We have to add the three zeros to work with HighCharts
              visits.append('[%s000,%s]' % (epoch, number['total']))
    
      visits = ', '.join(visits)
    
      jsonp += '{'
    
      jsonp += '"label": "%s",' % academic_career_name
    
      jsonp += '"value": "%s",' % visit_count
      
      jsonp += '"data": [%s]' % visits
      
      jsonp += '},'
    
    if(jsonp[-1:] != '['):
      jsonp = jsonp[:-1]
    
    jsonp += ']'
        
    jsonp += ',"meta":{'

    jsonp += '"library":["%s"],' % library

    jsonp += '"strt_date":["%s"],' % start

    jsonp += '"end_date":["%s"],' % end

    jsonp += '"title":["%s"]' % "Academic Career"

    jsonp += '}'

    jsonp += ',"queried_at": "%s"' % datetime.now()

    jsonp += '}'

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
