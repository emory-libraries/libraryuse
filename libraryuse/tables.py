import django_tables2 as tables
from models import LibraryVisit

class PersonTypeTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("prsn_e_type", "prsn_e_type__count")
        attrs = {"class": "paleblue"}
        prefix='pt_t_'
        
class DepartmentTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("dprt_n", "dprt_n__count")
        attrs = {"class": "paleblue"}
        prefix='dpt_t_'

class DivisionTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("dvsn_n", "dvsn_n__count")
        attrs = {"class": "paleblue"}
        prefix='div_t_'
        
class ProgramTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("acpr_n", "acpr_n__count")
        attrs = {"class": "paleblue"}
        prefix='pgm_t_'
        
class PlanTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("acpl_n", "acpl_n__count")
        attrs = {"class": "paleblue"}
        prefix='pln_t_'
        
class ClassTable(tables.Table):
    class Meta:
        model = LibraryVisit
        fields = ("stdn_e_clas", "stdn_e_clas__count")
        attrs = {"class": "paleblue"}
        prefix='cls_t_'
        
        