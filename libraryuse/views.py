from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response 
from django.template import RequestContext
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils import simplejson
import json
from django.shortcuts import redirect 
from django.db.models import Q, Count
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from datetime import timedelta
from django.core.exceptions import PermissionDenied
from django.core import serializers
import random, string, csv, sys
from forms import DataExportForm
from models import LibraryVisit
from libraryuse.tables import PersonTypeTable, DepartmentTable, DivisionTable, ProgramTable, PlanTable, ClassTable
from django_tables2 import RequestConfig

import pprint
import random
import string

from datetime import datetime
import time

@login_required
def index(request):
    context = {}
    return render_to_response('libraryuse/summary.html', context)

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
            #visits = LibraryVisit.objects.all()
            visits = LibraryVisit.objects.filter(visit_time__range=[start_date, end_date])
            #visits = LibraryVisit.objects.filter(Q(visit_time__range=[start_date, end_date]) and Q(acpl_n='Business Administration'))
            
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
        
    #q = LibraryVisit.objects.filter(visit_time__range=['2014-02-02', '2014-02-03'])
    #print('HELLO')
    #for r in q:
    #    print(r.location)

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

@login_required
def visualize(request):
    context = {}
    return render_to_response('libraryuse/visualize.html', context)

@login_required
def usage(request, dim):
    qset = _usage(dim)
    # {labels:[], datasets[{data}]}
    data= {}
    data['labels'] = []
    data['datasets'] = []
    dataset = {}
    dataset['data'] = []
    #data['datasets'].append('data')
    for e in qset.all():
        #print('type = %s, count = %s ' % (e['prsn_e_type'], e['prsn_e_type__count']))
        data['labels'].append(e['prsn_e_type'])
        dataset['data'].append(e['prsn_e_type__count'])
    data['datasets'].append(dataset)
    print(data)
    my_list = list(qset)
    data_json =  simplejson.dumps(data)
    return HttpResponse(data_json, content_type='application/json')

def chart_data(numbers):
    
    #randomstr = ''.join([random.choice(string.ascii_letters) for n in xrange(3)])
    
    data = []
    visits = []
    data.append('jsonResponse({"data":[')
    for number in numbers:
        dt = datetime.strptime(str(number['visit_time']), '%Y-%m-%d %H:%M:%S')
        epoch = int(time.mktime(dt.timetuple()))
        # We have to add the three zeros to work with HighCharts
        visits.append('[%s000,%s]' % (epoch, number['total']))
    data.append(', '.join(visits))
    data.append(']})')
    
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
    
    location = location_name(library)
    
    numbers = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time')).order_by('visit_time').filter(visit_time__range=[start, end]).filter(location = location)

    data = chart_data(numbers)

    return HttpResponse(data, content_type='application/json')

def total_distinct_usage(request, library, start, end):
    
    location = location_name(library)
    
    numbers = LibraryVisit.objects.values('visit_time').annotate(total=Count('prsn_i_ecn', distinct=True)).filter(visit_time__range=[start, end]).filter(location = location)

    data = chart_data(numbers)

    return StreamingHttpResponse(data, content_type='application/json')

def on_off_campus(request, library, resident, start, end):
    
    location = location_name(library)
    
    numbers = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time')).order_by('visit_time').filter(visit_time__range=[start, end]).filter(location = location).filter(stdn_f_cmps_on = resident).filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))

    data = chart_data(numbers)

    return HttpResponse(data, content_type='application/json')

def student_class(request, library, classification, start, end):
    
    location = location_name(library)
    
    numbers = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time')).order_by('visit_time').filter(visit_time__range=[start, end]).filter(location = location).filter(stdn_e_clas = classification).filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))

    data = chart_data(numbers)

    return HttpResponse(data, content_type='application/json')

def faculty_staff_class(request, library, classification, start, end):
    
    location = location_name(library)
    
    numbers = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time')).order_by('visit_time').filter(visit_time__range=[start, end]).filter(location = location).filter(prsn_e_type = classification)

    data = chart_data(numbers)

    return HttpResponse(data, content_type='application/json')

def classifications(request):
    student_classes = LibraryVisit.objects.values_list('stdn_e_clas', flat=True).distinct().exclude(stdn_e_clas__isnull=True)
    acidemic_plans = LibraryVisit.objects.values_list('acpl_n', flat=True).distinct().exclude(acpl_n__isnull=True)
    department = LibraryVisit.objects.values_list('dprt_n', flat=True).distinct().exclude(dprt_n__isnull=True)
    acc_career = LibraryVisit.objects.values_list('acca_i', flat=True).distinct().exclude(acca_i__isnull=True).filter(Q(prsn_c_type = 'C') | Q(prsn_c_type = 'B') | Q(prsn_c_type = 'E'))
    faculty_dvsn_n = LibraryVisit.objects.values_list('dvsn_n', flat=True).distinct().exclude(dvsn_n__isnull=True).filter(Q(prsn_c_type = 'F'))
    
    data = []
    json_data = []
    
    def add_classes(classes, title):
        list = [title]
        class_list = []
        
        for item in classes:
            class_list.append(str('%s' % item))
        
        list.append(class_list)
        return class_list
    
    #data.append('jsonCategories({')
    data.append(add_classes(student_classes, 'student_classes'))
    data.append(add_classes(acidemic_plans, 'acidemic_plans'))
    data.append(add_classes(acc_career, 'acdemic_career'))
    data.append(add_classes(faculty_dvsn_n, 'faculty_divisions'))
    #jsonp.append('jsonResponse({')
    json_data.append(json.dumps(data))
    #jsonp.append('})')
    jsonp = 'jsonClassifications(%s)' % data
    
    return StreamingHttpResponse(json_data, content_type='application/json')

#try tables.py, and count as string
def _usage(dim):
    def crunch(attr):
        #return LibraryVisit.objects.values(attr).annotate(Count(attr)).order_by('-%s__count' % attr).filter(visit_time__range=[start, end])
        return LibraryVisit.objects.values(attr).annotate(Count(attr)).order_by('-%s__count' % attr)

    result = None
    if dim == 'department':
        result = crunch('dprt_n')
    elif dim == 'division':
        result = crunch('dvsn_n')
    elif dim == 'person_type':        
        result = crunch('prsn_e_type')
    elif dim == 'program':
        result = crunch('acpr_n')
    elif dim == 'plan':
        result = crunch('acpl_n')
    elif dim == 'class':
        result = crunch('stdn_e_clas')
    #else return null  

    return result

def _values_query_set_to_dict(vqs):
    return [item for item in vqs]

@login_required
def _result_to_json(request, result):        
      
    data_dict = _values_query_set_to_dict(result)
    
    #evidently can't serialize ValuesQuerySet - surprising limitation 
    #data_json = serializers.serialize('json', data_dict)
    data_json =  simplejson.dumps(data_dict)

    return HttpResponse(data_json, content_type='application/json')

@login_required
def daterange_json(request):
    #q = LibraryVisit.objects.filter(visit_time__range=['2014-02-02', '2014-02-03'])
    #data_dict = _values_query_set_to_dict(q)
    pt_t = _usage('person_type')
    #RequestConfig(request).configure(pt_t)
    #pp = pprint.PrettyPrinter(depth=6)
    #pp.pprint(pt_t)
    #data_dict = _values_query_set_to_dict(pt_t)
    return HttpResponse(pt_t, content_type='application/json')
