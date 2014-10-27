from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from api.resources import ClassificationsResource
from libraryuse import views

admin.autodiscover()

v1_api = Api(api_name='v1')
#v1_api.register(VisitsResource())
#v1_api.register(VisitCountHalfHourResource())
#v1_api.register(VisitCountResource())
v1_api.register(ClassificationsResource())

urlpatterns = patterns(
    '',
    #url(r'^$', views.index, name='index'),

    url(r'^$', views.index, name='index'),
    url(r'^reports$', views.reports_index, name='reports_index'),
    #url(r'^summary$', views.summary, name='summary'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^export$', views.export, name='export'),

    url(r'^student_classifications', views.student_classifications, name='student_classifications'),
    url(r'^classifications', views.classifications, name='classifications'),

    url(r'^total_usage/(?P<library>.+)/(?P<person_type>.+)/(?P<start>.+)/(?P<end>.+)/$', views.total_usage, name='total_usage'),
    url(r'^on_off_campus/(?P<library>.+)/(?P<resident>.+)/(?P<start>.+)/(?P<end>.+)/$', views.on_off_campus, name='on_off_campus'),
    url(r'^student_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.student_class, name='student_class'),
    url(r'^faculty_staff_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.faculty_staff_class, name='faculty_staff_class'),
    url(r'^degree_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.degree_class, name='degree_class'),
    url(r'^career_class/(?P<library>.+)/(?P<classification>.+)/(?P<start>.+)/(?P<end>.+)/$', views.career_class, name='career_class'),

    url(r'^top_academic_plan/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_academic_plan, name='top_academic_plan'),
    url(r'^top_academic_career/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_academic_career, name='top_academic_career'),

    url(r'^top_dprtn/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_dprtn, name='top_dprtn'),
    url(r'^top_dprtn_type/(?P<library>.+)/(?P<person_type>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_dprtn_type, name='top_dprtn_type'),

    url(r'^top_division/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_division, name='top_division'),
    url(r'^top_division_type/(?P<library>.+)/(?P<person_type>.+)/(?P<start>.+)/(?P<end>.+)/$', views.top_division_type, name='top_division_type'),

    url(r'^averages/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/(?P<start_hour>.+)/(?P<end_hour>.+)/(?P<dow>.+)/(?P<filter_on>.+)/$', views.averages, name='averages'),
    url(r'^total_averages/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/(?P<start_hour>.+)/(?P<end_hour>.+)/(?P<dow>.+)/$', views.total_averages, name='total_averages'),

    url(r'^faculty_divs_dprt/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.faculty_divs_dprt, name='faculty_divs_dprt'),
    url(r'^faculty_dprt_count/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.faculty_dprt_count, name='faculty_dprt_count'),

    url(r'^classification_totals/(?P<library>.+)/(?P<person_type>.+)/(?P<start>.+)/(?P<end>.+)/$', views.classification_totals, name='classification_totals'),

    url(r'^export/(?P<start>.+)/(?P<end>.+)/$', views.export, name='export'),

    url(r'^api/', include(v1_api.urls)),

    url(r'^login/$', views.login_user, name='login_user'),

    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/'}),
)
