API
===

.. automodule:: libraryuse

Libraries
---------
* woodruff
* law
* health

Date formats
------------
* YYYY-MM-DD

Total usage by library
----------------------
`/total_usage/<library>/<person type>/<start date>/<end date>/`

Person Types:
^^^^^^^^^^^^^
* all
* student
* faculty
* staff

Filtered by:
^^^^^^^^^^^^
* Library
* persn_c_type

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: totalusage.json

Total students living on or off campus by library
-------------------------------------------------
`/on_off_campus/<library>/<Y/N>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* stdn_f_cmps_on
* prsn_c_type (students only)

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: on_off_campus.json

Totals by student classifications by library
--------------------------------------------
`/student_class/<library>/<stdn_e_clas>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* stdn_e_clas
* prsn_c_type (students only)

Totals by faculty classifications by library
--------------------------------------------
`/faculty_staff_class/<library>/<dvsn_n>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dvsn_n
* prsn_c_type (faculty only)

Top Academic Plans
------------------
`/top_academic_plan/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* acpl_n
* prsn_c_type (students only)

Top Departments
---------------
`/top_dprtn/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dprt_n

Top Divisions
-------------
`/top_division/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dvsn_n

Average by day, hour(s) and classification
------------------------------------------
`/total_averages/<library>/<start date>/<end date>/<start hour>/<end hour>/<dow>/<filter>`

* Hours are 0 - 23
* Days are ints with Sunday = 1...Saturday = 7
Filters:
^^^^^^^^
* stdn_e_clas (student_classes)
* acpl_n (acidemic_plans)
* dprt_n (departments)
* acca_i (academic_career)
* dvsn_n (faculty_divisions)

Total Average by day and hour(s)
--------------------------------
`/total_averages/<library>/<start date>/<end date>/<start hour>/<end hour>/<dow>`
* Hours are 0 - 23
* Days are ints with Sunday = 1...Saturday = 7

Classifications
---------------
`/classifications`

* student_classes = stdn_e_clas
* acidemic_plans = acpl_n
* departments = dprt_n
* academic_career = acca_i
* faculty_divisions = dvsn_n
