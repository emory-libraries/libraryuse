from datetime import timedelta
from django import forms
from django.db import models
import datetime
from django.contrib.auth import authenticate

class DataExport(models.Model):
    start_date = models.DateField('start date', null=True, blank=True)
    end_date = models.DateField('end date', null=True, blank=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    username.widget = forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Username",
        "required":"required"
      })
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password.widget = forms.PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Password",
        "required":"required"
    })

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username or not password:
          raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
          return self.cleaned_data
        user = authenticate(username=username, password=password)
        if not user or not user.is_active or user == None:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class LibraryVisitKey(models.Model):
    LIBRARY_VISIT_KEY_CHOICES = (
        ('visit_time', 'Time through the turnstile'),
        ('term_number', 'Get term code definition from etd'),
        ('prsn_i_pblc', 'Public identifier of the person  (PPID)'),
        ('prsn_i_ecn', 'EmoryCard number identifier of the person'),
        ('prsn_i_hr', 'HR (emplid) identifier of the person'),
        ('prsn8hc_i_hr', 'Healthcare HR (emplid) identifier of the person'),
        ('prsn_i_sa', 'SA (emplid) identifier of the person'),
        ('prsn_e_titl_dtry', 'directory title of the person'),
        ('prsn_c_type', 'EU type code of the person'),
        ('prsn_e_type', 'EU type description of the person'),
        ('emjo_c_clsf', 'EU classification code of the employee job (primary)'),
        ('dprt_c', 'EU department code of the primary job'),
        ('dprt_n', 'EU department name of the primary job'),
        ('dvsn_i', 'EU division identifier of the primary job'),
        ('dvsn_n', 'EU division name of the the primary job'),
        ('empe_c_fclt_rank', 'EU faculty rank code'),
        ('prsn_c_type_hc', 'HC type code of the person'),
        ('prsn_e_type_hc', 'HC type description of the person'),
        ('emjo8hc_c_clsf', 'HC classification code of the employee job'),
        ('dprt8hc_c', 'HC department code of the employee job'),
        ('dprt8hc_n', 'HC department name of the employee job'),
        ('dvsn8hc_i', 'HC division identifier of the employee job'),
        ('dvsn8hc_n', 'HC division name of the employee job'),
        ('acca_i', 'Academic career identifier of the student (primary)'),
        ('acpr_n', 'Academic program name of the student '),
        ('acpl_n', 'Academic plan name of the student'),
        ('stdn_e_clas', 'Class description of the student'),
        ('stdn_f_ungr', 'Undergraduate flag of the student'),
        ('stdn_f_cmps_on', 'On-campus flag of the student'),
    )
    key = models.CharField(max_length=30, choices=LIBRARY_VISIT_KEY_CHOICES)

class LibraryVisit(models.Model):
    prsn_i_pblc = models.CharField(max_length=32L, db_column='PRSN_I_PBLC', null=True) #md5 hash of public identifier of person
    prsn_i_ecn = models.CharField(max_length=32L, db_column='PRSN_I_ECN', null=True) #md5 hash of EmoryCard number
    prsn_i_hr = models.CharField(max_length=7L, db_column='PRSN_I_HR', null=True) #HR (emplid) of person
    prsn8hc_i_hr = models.CharField(max_length=7L, db_column='PRSN8HC_I_HR', null=True) #Healthcare HR ID (emplid) of person
    prsn_i_sa = models.CharField(max_length=7L, db_column='PRSN_I_SA', null=True) #SA (emplid) of the person
    prsn_e_titl_dtry = models.CharField(max_length=70L, db_column='PRSN_E_TITL_DTRY', null=True) #directory title of person
    visit_time = models.DateTimeField() #"normalized" to minute to minimize multiswipe entrances
    location = models.CharField(max_length=80L)
    prsn_c_type = models.CharField(max_length=1L, db_column='PRSN_C_TYPE', null=True) #EU type code of the person
    prsn_e_type = models.CharField(max_length=30L, db_column='PRSN_E_TYPE', null=True) #EU type description of the person
    emjo_c_clsf = models.CharField(max_length=1L, db_column='EMJO_C_CLSF', null=True) #EU classification code of the employee job (primary)
    dprt_c = models.CharField(max_length=10L, db_column='DPRT_C', null=True) #EU department code of the primary job
    dprt_n = models.CharField(max_length=40L, db_column='DPRT_N', null=True) #EU department name of the primary job
    dvsn_i = models.CharField(max_length=10L, db_column='DVSN_I', null=True) #EU division identifier of the primary job
    dvsn_n = models.CharField(max_length=40L, db_column='DVSN_N', null=True) #EU division name of the the primary job
    empe_c_fclt_rank = models.CharField(max_length=2L, db_column='EMPE_C_FCLT_RANK', null=True) #EU faculty rank code
    prsn_c_type_hc = models.CharField(max_length=1L, db_column='PRSN_C_TYPE_HC', null=True) #HC type code of the person
    prsn_e_type_hc = models.CharField(max_length=30L, db_column='PRSN_E_TYPE_HC', null=True) #HC type description of the person
    emjo8hc_c_clsf = models.CharField(max_length=1L, db_column='EMJO8HC_C_CLSF', null=True) #HC classification code of the employee job
    dprt8hc_c = models.CharField(max_length=10L, db_column='DPRT8HC_C', null=True) #HC department code of the employee job
    dprt8hc_n = models.CharField(max_length=40L, db_column='DPRT8HC_N', null=True) #HC department name of the employee job
    dvsn8hc_i = models.CharField(max_length=10L, db_column='DVSN8HC_I', null=True) #HC division identifier of the employee job
    dvsn8hc_n = models.CharField(max_length=40L, db_column='DVSN8HC_N', null=True) #HC division name of the employee job
    acca_i = models.CharField(max_length=4L, db_column='ACCA_I', null=True) #Academic career identifier of the student (primary)
    acpr_n = models.CharField(max_length=30L, db_column='ACPR_N', null=True) #Academic program name of the student
    acpl_n = models.CharField(max_length=30L, db_column='ACPL_N', null=True) #Academic plan name of the student
    stdn_e_clas = models.CharField(max_length=30L, db_column='STDN_E_CLAS', null=True) #Class description of the student
    stdn_f_ungr = models.CharField(max_length=1L, db_column='STDN_F_UNGR', null=True) #Undergraduate flag of the student
    stdn_f_cmps_on = models.CharField(max_length=1L, db_column='STDN_F_CMPS_ON', null=True) #On-campus flag of the student

    class Meta:
        managed = False
        db_table = 'libraryvisit_mv'
        app_label = 'libraryuse'
