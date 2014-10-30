from django.contrib import admin
from models import LibraryVisit

class LibraryAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(LibraryVisit, LibraryAdmin)
