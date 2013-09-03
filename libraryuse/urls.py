from django.conf.urls import patterns, include, url
from django.contrib import admin
from libraryuse import views, settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^export$', views.export, name='export'),
    url(r'^reports$', views.reports, name='reports'),
    url(r'^usage/(?P<dim>.+)/$', views.get_usage, name='usage'),
    url(r'^test$', views.test, name='test'),
)
