# file libraryuse/libraryuse/management/commands/dbops.py
# 
#   Copyright 2013 Emory University General Library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import generators 

from libraryuse import settings
import logging
from optparse import make_option
import sys
import os
from datetime import timedelta
import cx_Oracle
from django.db import connection, connections, transaction
from django.core.management.base import BaseCommand, CommandError
from libraryuse.models import LibraryVisit
from django.db.models import Max

class Command(BaseCommand):
    help = "perform database maintenance operations"

    option_list = BaseCommand.option_list + (
        make_option('--refresh-esd',
            action='store_true',
            dest='refresh_esd',
            default=False,
            help='Refresh Emory Shared Data copy'),
        make_option('--refresh-libraryvisit',
            action='store_true',
            dest='refresh_libraryvisit',
            default=False,
            help='Refresh libraryvisit_mv materialized view'),
        make_option('--update-libraryvisit',
            action='store_true',
            dest='update_libraryvisit',
            default=False,
            help='Update libraryvisit_mv materialized view'),
        )

    @transaction.commit_manually
    def handle(self, *args, **options):
        if not (options['refresh_esd'] or options['refresh_libraryvisit'] or options['update_libraryvisit']):
            sys.exit('Nothing to do')
        
        if options['refresh_esd']:
            self.refresh_esd()
        if options['refresh_libraryvisit']:
            self.refresh_libraryvisit()
        if options['update_libraryvisit']:
            self.update_libraryvisit()

    @transaction.commit_manually
    def refresh_esd(self):
        cxn_esd = connections['esd']
        cursor_esd = cxn_esd.cursor()
        #cursor_esd.execute("select * from V_LUD_PRSN where rownum <= 10")
        cursor_esd.execute("select * from V_LUD_PRSN")
        
        cxn_db = connections['default']
        cursor_db = cxn_db.cursor()

        try:
            cursor_db.execute("truncate esd")
            for result in self.ResultsIterator(cursor_esd):
                cursor_db.execute('''insert into esd (PRSN_I_PBLC, PRSN_I_ECN,  
                PRSN_I_HR, PRSN8HC_I_HR, PRSN_I_SA, PRSN_E_TITL_DTRY, PRSN_C_TYPE, 
                PRSN_E_TYPE, EMJO_C_CLSF, DPRT_C, DPRT_N, DVSN_I, DVSN_N, 
                EMPE_C_FCLT_RANK, PRSN_C_TYPE_HC, PRSN_E_TYPE_HC, EMJO8HC_C_CLSF, 
                DPRT8HC_C, DPRT8HC_N, DVSN8HC_I, DVSN8HC_N, ACCA_I, ACPR_N, 
                ACPL_N, STDN_E_CLAS, STDN_F_UNGR, STDN_F_CMPS_ON) values ( 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', result)
    
        except Exception, e:
            transaction.rollback()
            cxn_esd.close()
            cxn_db.close()
            raise CommandError("problem refreshing db.esd: %s" % e)

        transaction.commit()
        cxn_esd.close()
        cxn_db.close()
 
    @transaction.commit_manually
    def refresh_libraryvisit(self):

        cxn_db = connections['default']
        cursor_db = cxn_db.cursor()

        try:
            try:
                cursor_db.execute("drop table libraryvisit_mv")
            except:
                sys.exc_clear() #no problem

            cmd = ('''create table libraryvisit_mv 
            as select distinct concat(idnumber,substr(term_date,1,16)) as id, 
            idnumber, lastname, firstname, 
            str_to_date(concat(substr(term_date,1,16),':00'), '%Y-%m-%d %T') as visit_time,
            location, term_number, PRSN_I_PBLC, PRSN_I_ECN, PRSN_I_HR, PRSN8HC_I_HR, 
            PRSN_I_SA, PRSN_E_TITL_DTRY, PRSN_C_TYPE, PRSN_E_TYPE, 
            EMJO_C_CLSF, DPRT_C, DPRT_N, DVSN_I, DVSN_N, EMPE_C_FCLT_RANK, 
            PRSN_C_TYPE_HC, PRSN_E_TYPE_HC, EMJO8HC_C_CLSF, DPRT8HC_C, 
            DPRT8HC_N, DVSN8HC_I, DVSN8HC_N, ACCA_I, ACPR_N, ACPL_N, 
            STDN_E_CLAS, STDN_F_UNGR, STDN_F_CMPS_ON  
            from turnstile, esd 
            where replace(turnstile.idnumber,' ', '') = esd.PRSN_I_ECN;''')
            
            cursor_db.execute(cmd)
    
        except Exception, e:
            transaction.rollback()
            cxn_db.close()
            raise CommandError("problem refreshing db.libraryvisit_mv: %s" % e)

        transaction.commit()
        cxn_db.close()
    
    @transaction.commit_manually
    def update_libraryvisit(self):

        cxn_db = connections['default']
        cursor_db = cxn_db.cursor()
        
        last_date = LibraryVisit.objects.all().aggregate(Max('visit_time'))
        search_date = last_date['visit_time__max'] + timedelta(minutes=1)

        try:
            
            cmd = '''INSERT INTO libraryvisit_mv (id, idnumber, lastname, firstname,
            visit_time, location, term_number, prsn_i_pblc, prsn_i_ecn,  
            prsn_i_hr, prsn8hc_i_hr, prsn_i_sa, prsn_e_titl_dtry, prsn_c_type, 
            prsn_e_type, emjo_c_clsf, dprt_c, dprt_n, dvsn_i, dvsn_n, 
            empe_c_fclt_rank, prsn_c_type_hc, prsn_e_type_hc, emjo8hc_c_clsf, 
            dprt8hc_c, dprt8hc_n, dvsn8hc_i, dvsn8hc_n, acca_i, acpr_n, 
            acpl_n, stdn_e_clas, stdn_f_ungr, stdn_f_cmps_on)
            
            (SELECT concat(turnstile.idnumber,substr(turnstile.term_date,1,16)),
            turnstile.idnumber, turnstile.lastname, turnstile.firstname,
            str_to_date(concat(substr(turnstile.term_date,1,16),':00'), '%%Y-%%m-%%d %%T'),
            turnstile.location, turnstile.term_number, esd.prsn_i_pblc, esd.prsn_i_ecn, esd.prsn_i_hr, esd.prsn8hc_i_hr,
            esd.prsn_i_sa, esd.prsn_e_titl_dtry, esd.prsn_c_type, esd.prsn_e_type,
            esd.emjo_c_clsf, esd.dprt_c, esd.dprt_n, esd.dvsn_i, esd.dvsn_n, 
            esd.empe_c_fclt_rank, esd.prsn_c_type_hc, esd.prsn_e_type_hc, esd.emjo8hc_c_clsf, 
            esd.dprt8hc_c, esd.dprt8hc_n, esd.dvsn8hc_i, esd.dvsn8hc_n, esd.acca_i, esd.acpr_n, 
            esd.acpl_n, esd.stdn_e_clas, esd.stdn_f_ungr, esd.stdn_f_cmps_on
            
            FROM turnstile, esd 
            
            WHERE (replace(turnstile.idnumber,' ', '') = esd.prsn_i_ecn) AND (DATE(turnstile.term_date) > '%s'));''' % (search_date)
            
            cursor_db.execute(cmd)
    
        except Exception, e:
            transaction.rollback()
            cxn_db.close()
            raise CommandError("problem refreshing db.libraryvisit_mv: %s" % e)

        transaction.commit()
        cxn_db.close()
        
    def ResultsIterator(self, cursor, howmany=1000):
        while True:
            results = cursor.fetchmany(howmany)
            if not results:
                break
            for result in results:
                yield result