from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.shortcuts import render_to_response 
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils import simplejson
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

def index(request):
    context = {}
    return render_to_response('libraryuse/summary.html', context)

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
            #visits = LibraryVisit.objects.all()
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
        
    return render_to_response('libraryuse/export.html', context)

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

def visualize(request):
    context = {}
    return render_to_response('libraryuse/visualize.html', context)

def usage(request, dim):
    return HttpResponse(_usage(dim), content_type='application/json')

#try tables.py, and count as string
def _usage(dim):
    
    def crunch(attr):
        #return LibraryVisit.objects.values(attr).annotate(Count(attr)).order_by('-%s__count' % attr).values()
        
        return LibraryVisit.objects.values(attr).annotate(Count(attr)).order_by('-%s__count' % attr)
        #.extra(select={'percent': 'count(prsn_e_type)* 100 /(select count(*) from libraryvisit_mv)'})
        
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

def _result_to_json(request, result):        
      
    data_dict = _values_query_set_to_dict(result)
    
    #evidently can't serialize ValuesQuerySet - surprising limitation 
    #data_json = serializers.serialize('json', data_dict)
    data_json =  simplejson.dumps(data_dict)

    return HttpResponse(data_json, content_type='application/json')

    