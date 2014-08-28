from tastypie import authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL
#from libraryuse.documents import Visits, VisitMinute, VisitHalfHour, VisitCountHalfHour
from libraryuse.models import LibraryVisit
from django.db.models import Count

class ClassificationsResource(ModelResource):

    #def apply_filters(self, request, applicable_filters):
    """
    An ORM-specific implementation of ``apply_filters``.

    The default simply applies the ``applicable_filters`` as ``**kwargs``,
    but should make it possible to do more advanced things.

    Here we override to check for a 'distinct' query string variable,
    if it's equal to True we apply distinct() to the queryset after filtering.
    """
        # distinct = request.GET.get('distinct', True) == 'True'
        # if distinct:
        #     return self.get_object_list(request).filter(**applicable_filters).distinct()
        # else:
        #     return self.get_object_list(request).filter(**applicable_filters)

    class Meta:
        queryset = LibraryVisit.objects.all().exclude(stdn_e_clas__isnull=True)
        #queryset = LibraryVisit.objects.values_list().distinct().exclude(stdn_e_clas__isnull=True)
        allowed_methods = ('get')
        resource_name = 'classifications'
        authorization = authorization.ReadOnlyAuthorization()
        fields = ['stdn_e_clas']
        filtering = {
            'stdn_e_clas': ('distinct')
        }
    # def get_object_list(self, request):
    #     return super(ClassificationsResource, self).get_object_list(request).annotate(queryset=Count('stdn_e_clas', distinct=True))

#class VisitCountHalfHourResource(resources.MongoEngineResource):
#
#    class Meta:
#        queryset = VisitCountHalfHour.objects.all()
#        allowed_methods = ('get')
#        resource_name = 'visitcounthalfhour'
#        authorization = authorization.ReadOnlyAuthorization()
#        filtering = {
#            'visit_time': ('lte', 'gte'),
#            'location': ('exact'),
#        }
#
#class VisitsResource(resources.MongoEngineResource):
#
#    class Meta:
#        queryset = Visits.objects.all()
#        allowed_methods = ('get')
#        resource_name = 'visits'
#        authorization = authorization.ReadOnlyAuthorization()
#        filtering = {
#            'visit_time': ALL,
#            'location': ALL,
#        }
#
#class VisitCountResource(ModelResource):
#    class Meta:
#        #queryset = LibraryVisit.objects.values('visit_time').annotate(total=Count('visit_time'))
#        queryset = LibraryVisit.objects.all()
#        allowed_methods = ('get')
#        resource_name = 'visitcount'
#        authorization = authorization.ReadOnlyAuthorization()
#        filtering = {
#            'visit_time': ('lte', 'gte'),
#            'location': ('exact'),
#        }
