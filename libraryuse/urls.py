from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from api.resources import VisitsResource, VisitCountHalfHourResource, VisitCountResource
from libraryuse import views, settings

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(VisitsResource())
v1_api.register(VisitCountHalfHourResource())
v1_api.register(VisitCountResource())

urlpatterns = patterns(
    '',
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.summary, name='index'),
    url(r'^summary$', views.summary, name='summary'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^export$', views.export, name='export'),
    url(r'^visualize$', views.visualize, name='visualize'),
    url(r'^usage/(?P<dim>.+)/(?P<start>.+)/(?P<end>.+)/$', views.usage, name='usage'),
    url(r'^usage_json/(?P<library>.+)/(?P<start>.+)/(?P<end>.+)/$', views.usage_json, name='usage_json'),
    url(r'^daterange_json$', views.daterange_json, name='daterange'),
    url(r'^api/', include(v1_api.urls)),
)
