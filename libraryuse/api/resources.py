from tastypie_mongoengine import resources
from tastypie import authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
from libraryuse.documents import Visits, VisitMinute, VisitHalfHour, VisitCountHalfHour
from libraryuse.models import LibraryVisit
from django.db.models import Count

class VisitCountHalfHourResource(resources.MongoEngineResource):
    
    class Meta:
        queryset = VisitCountHalfHour.objects.all()
        allowed_methods = ('get')
        resource_name = 'visitcounthalfhour'
        authorization = authorization.ReadOnlyAuthorization()
        filtering = {
            'visit_time': ('lte', 'gte'),
            'location': ('exact'),
        }

class VisitsResource(resources.MongoEngineResource):

    class Meta:
        queryset = Visits.objects.all()
        allowed_methods = ('get')
        resource_name = 'visits'
        authorization = authorization.ReadOnlyAuthorization()
        filtering = {
            'visit_time': ALL,
            'location': ALL,
        }

class VisitCountResource(ModelResource):
    class Meta:
        #queryset = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time'))
        queryset = LibraryVisit.objects.all()
        allowed_methods = ('get')
        resource_name = 'visitcount'
        authorization = authorization.ReadOnlyAuthorization()
        filtering = {
            'visit_time': ('lte', 'gte'),
            'location': ('exact'),
        }
