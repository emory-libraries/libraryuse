from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from api.resources import ClassificationsResource
from libraryuse import views, settings

admin.autodiscover()

v1_api = Api(api_name='v1')
#v1_api.register(VisitsResource())
#v1_api.register(VisitCountHalfHourResource())
#v1_api.register(VisitCountResource())
v1_api.register(ClassificationsResource())

urlpatterns = patterns(
    '',
    #url(r'^$', views.index, name='index'),
    
    url(r'^$', views.summary, name='index'),
    url(r'^summary$', views.summary, name='summary'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^export$', views.export, name='export'),
    url(r'^visualize$', views.visualize, name='visualize'),
    
    url(r'^student_classifications', views.student_classifications, name='student_classifications'),
    url(r'^classifications', views.classifications, name='classifications'),
    
    url(r'^usage/(?P<dim>.+)/(?P<start>.+)/(?P<end>.+)/$', views.usage, name='usage'),
    url(r'^total_usage/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.total_usage, name='total_usage'),
    url(r'^daterange_json$', views.daterange_json, name='daterange'),
    url(r'^on_off_campus/(?P<library>.+)/(?P<resident>.+)/(?P<start>.+)/(?P<end>.+)/$', views.on_off_campus, name='on_off_campus'),
    url(r'^student_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.student_class, name='student_class'),
    url(r'^faculty_staff_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.faculty_staff_class, name='faculty_staff_class'),
    url(r'^top_academic_plan/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_academic_plan, name='top_academic_plan'),
    url(r'^top_dprtn/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_dprtn, name='top_dprtn'),
    url(r'^top_devision/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_devision, name='top_devision'),
    url(r'^averages/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/(?P<start_hour>.+)/(?P<end_hour>.+)/(?P<dow>.+)/$', views.averages, name='averages'),

    url(r'^api/', include(v1_api.urls)),
)
