from django.conf import settings

class DBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.object_name == 'EmoryPersonInfo':
            return 'esd'
        
    def allow_relation(self, obj1, obj2, **hints):
        if  ((obj1._meta.object_name == 'EmoryPersonInfo' and 
              obj2._meta.object_name == 'LibraryVisit') or
             (obj2._meta.object_name == 'EmoryPersonInfo' and 
              obj1._meta.object_name == 'LibraryVisit')):
            
            return true

