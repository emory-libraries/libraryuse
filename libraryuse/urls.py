from django.conf.urls import patterns, include, url
from django.contrib import admin
from libraryuse import views, settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    #url(r'^$', views.index, name='index'),
    url(r'^$', views.summary, name='index'),
    url(r'^summary$', views.summary, name='summary'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^export$', views.export, name='export'),
    url(r'^visualize$', views.visualize, name='visualize'),
    url(r'^usage/(?P<dim>.+)/$', views.usage, name='usage'),
)
