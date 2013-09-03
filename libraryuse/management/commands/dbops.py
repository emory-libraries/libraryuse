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
import cx_Oracle
from django.db import connection, connections, transaction
from django.core.management.base import BaseCommand, CommandError

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
        )

    @transaction.commit_manually
    def handle(self, *args, **options):
        if not (options['refresh_esd'] or options['refresh_libraryvisit']):
            sys.exit('Nothing to do')
        
        if options['refresh_esd']:
            self.refresh_esd()
        if options['refresh_libraryvisit']:
            self.refresh_libraryvisit()

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

            cursor_db.execute('''create table libraryvisit_mv 
            as select distinct concat(idnumber,substr(term_date,1,16)) as id, 
            idnumber, lastname, firstname, 
            concat(substr(term_date,1,16),':00') as visit_time, location, 
            term_number, PRSN_I_PBLC, PRSN_I_ECN, PRSN_I_HR, PRSN8HC_I_HR, 
            PRSN_I_SA, PRSN_E_TITL_DTRY, PRSN_C_TYPE, PRSN_E_TYPE, 
            EMJO_C_CLSF, DPRT_C, DPRT_N, DVSN_I, DVSN_N, EMPE_C_FCLT_RANK, 
            PRSN_C_TYPE_HC, PRSN_E_TYPE_HC, EMJO8HC_C_CLSF, DPRT8HC_C, 
            DPRT8HC_N, DVSN8HC_I, DVSN8HC_N, ACCA_I, ACPR_N, ACPL_N, 
            STDN_E_CLAS, STDN_F_UNGR, STDN_F_CMPS_ON  
            from turnstile, esd 
            where replace(turnstile.idnumber,' ', '') = esd.PRSN_I_ECN;''')
    
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

