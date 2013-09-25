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

def index(request):
    context = RequestContext(request, {})
    export_form = DataExportForm(request.POST)
    if export_form.is_valid():
        context = RequestContext(request, {'form': export_form})
    
    return render_to_response('libraryuse/home.html', context)

def get_usage(request, dim):
    context = RequestContext(request, {})
    
    result = None
    if dim == 'department':
        result = LibraryVisit.objects.values('dprt_n').annotate(Count('dprt_n')).order_by('-dprt_n__count')
    elif dim == 'division':
        result = LibraryVisit.objects.values('dvsn_n').annotate(Count('dvsn_n')).order_by('-dvsn_n__count')
    elif dim == 'prsntype':
        result = LibraryVisit.objects.values('prsn_e_type').annotate(Count('prsn_e_type')).order_by('-prsn_e_type__count')     
        
    #evidently can't serialize ValuesQuerySet - surprising limitation   
    data_dict = ValuesQuerySetToDict(result)
    #data_json = serializers.serialize('json', data_dict)
    data_json =  simplejson.dumps(data_dict)

    return HttpResponse(data_json, content_type='application/json')

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

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

def reports(request):
    #context = RequestContext(request, {'dept_data': get_usage(request, 'department') })
    context = {}
    return render_to_response('libraryuse/reports.html', context)

def test(request):
    context = {}
    return render_to_response('libraryuse/simple-pie.html', context)


    
    