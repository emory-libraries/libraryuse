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

Field Names
-----------

Emory Shared Data Fields
^^^^^^^^^^^^^^^^^^^^^^^^

The field names for the filters are based on Emory Shared Data (ESD):

+----------------+-----------------------------------------------------+
| ESD Field      | Explination                                         |
+================+=====================================================+
| prsn_i_ecn     | EmoryCard number identifer of person (Hashed in DB  |
+----------------+-----------------------------------------------------+
| prsn_c_type    | EU type code of the person                          |
+----------------+-----------------------------------------------------+
| prsn_e_type    | EU type description of the person                   |
+----------------+-----------------------------------------------------+
| dprt_c         | EU department code of the primary job               |
+----------------+-----------------------------------------------------+
| dprt_n         | EU department name of the primary job               |
+----------------+-----------------------------------------------------+
| dvsn_i         | EU division identifier of the primary job           |
+----------------+-----------------------------------------------------+
| dvsn_n         | EU division name of the the primary job             |
+----------------+-----------------------------------------------------+
| acca_i         | Academic career identifier of the student (primary) |
+----------------+-----------------------------------------------------+
| acpr_n         | Academic program name of the student                |
+----------------+-----------------------------------------------------+
| acpl_n         | Academic plan name of the student                   |
+----------------+-----------------------------------------------------+
| stdn_e_clas    | Class description of the student                    |
+----------------+-----------------------------------------------------+
| stdn_f_cmps_on | On-campus flag of the student                       |
+----------------+-----------------------------------------------------+

These are fields we are not using anywhere but do exist in the data:

+------------------+------------------------------------------------------+
| ESD Field        | Explination                                          |
+==================+======================================================+
| prsn_i_pblc      | Public identifier of the person (PPID) (Hashed in DB |
+------------------+------------------------------------------------------+
| prsn_i_hr        | HR (emplid) identifier of the person                 |
+------------------+------------------------------------------------------+
| prsn8hc_i_hr     | Healthcare HR (emplid) identifier of the person      |
+------------------+------------------------------------------------------+
| prsn_i_sa        | SA (emplid) identifier of the person                 |
+------------------+------------------------------------------------------+
| prsn_e_titl_dtry | directory title of the person                        |
+------------------+------------------------------------------------------+
| emjo_c_clsf      | EU classification code of the employee job (primary) |
+------------------+------------------------------------------------------+
| dprt_c           | EU department code of the primary job                |
+------------------+------------------------------------------------------+
| empe_c_fclt_rank | EU faculty rank code                                 |
+------------------+------------------------------------------------------+
| prsn_c_type_hc   | HC type code of the person                           |
+------------------+------------------------------------------------------+
| prsn_e_type_hc   | HC type description of the person                    |
+------------------+------------------------------------------------------+
| emjo8hc_c_clsf   | HC classification code of the employee job           |
+------------------+------------------------------------------------------+
| dprt8hc_c        | HC department code of the employee jobt              |
+------------------+------------------------------------------------------+
| dprt8hc_n        | HC department name of the employee job               |
+------------------+------------------------------------------------------+
| dvsn8hc_i        | HC division identifier of the employee job           |
+------------------+------------------------------------------------------+
| dvsn8hc_n        | HC division name of the employee job                 |
+------------------+------------------------------------------------------+
| acpr_n           | Academic program name of the student                 |
+------------------+------------------------------------------------------+
| stdn_f_ungr      | Undergraduate flag of the student                    |
+------------------+------------------------------------------------------+

Person Type codes
^^^^^^^^^^^^^^^^^

These are the codes for the *prsn_e_type* from ESD.

We use **B** and **S** to filter for students, **F** for faculty and **E** for staff. No other codes are used.

+---+-------------------+
| A | administrative    |
+---+-------------------+
| B | student/staff     |
+---+-------------------+
| C | staff/student     |
+---+-------------------+
| E | staff             |
+---+-------------------+
| F | faculty           |
+---+-------------------+
| J | EU job eligible   |
+---+-------------------+
| O | student applicant |
+---+-------------------+
| P | sponsored         |
+---+-------------------+
| R | retired           |
+---+-------------------+
| S | student           |
+---+-------------------+
| U | unknown           |
+---+-------------------+
| X | pre-start         |
+---+-------------------+

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
.. literalinclude:: sample_json/totalusage.json

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
.. literalinclude:: sample_json/on_off_campus.json

Totals by student classifications by library
--------------------------------------------
`/student_class/<library>/<stdn_e_clas>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* stdn_e_clas (*all* or a specified)
* prsn_c_type (students only)

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: sample_json/student_class.json

Totals by faculty classifications by library
--------------------------------------------
`/faculty_staff_class/<library>/<dvsn_n>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dvsn_n (*all* or a specified)
* prsn_c_type (faculty only)

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: sample_json/faculty_staff_class.json

Degree Class
------------
`/degree_class/<library>/<classificatino>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* acpl_n (*all* or a specified)
* prsn_c_type (students, faculty and staff)

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: sample_json/degree_class.json

Career Class
------------
`/career_class/<library>/<classificatino>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* acca_i (*all* or a specified)
* prsn_c_type (students, faculty and staff)

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: sample_json/career_class.json

Top Academic Plans
------------------
`/top_academic_plan/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* acpl_n
* prsn_c_type (students, faculty and staff)

Ordered by:
^^^^^^^^^^^
* Count of acpl_n

Example output:
^^^^^^^^^^^^^^^
.. literalinclude:: sample_json/top_academic_plan.json

Top Departments
---------------
`/top_dprtn/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dprt_n

Ordered by:
^^^^^^^^^^^
* Count of dprt_n

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/top_dprtn.json

Top Divisions
-------------
`/top_division/<library>/<start date>/<end date>/`

Filtered by:
^^^^^^^^^^^^
* Library
* dvsn_n

Ordered by:
^^^^^^^^^^^
* Count of dvsn_n

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/top_division.json

Top Division Type
-----------------
`/top_division/<library>/<start date>/<end date>/`

Person Types:
^^^^^^^^^^^^^
* all
* student
* faculty
* staff

Filtered by:
^^^^^^^^^^^^
* Library
* dvsn_n

Ordered by:
^^^^^^^^^^^
* Count of dvsn_n

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/top_division_type.json

Average by day, hour(s) and classification
------------------------------------------
`/averages/<library>/<start date>/<end date>/<start hour>/<end hour>/<dow>/<filter>`

* Hours are 0 - 23
* Days are ints with Sunday = 1...Saturday = 7

Filters:
^^^^^^^^
* stdn_e_clas (student_classes)
* acpl_n (acidemic_plans)
* dprt_n (departments)
* acca_i (academic_career)
* dvsn_n (faculty_divisions)

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/averages.json

Total Average by day and hour(s)
--------------------------------
`/total_averages/<library>/<start date>/<end date>/<start hour>/<end hour>/<dow>`
* Hours are 0 - 23
* Days are ints with Sunday = 1...Saturday = 7

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/total_averages.json

Classifications
---------------
`/classifications`

* student_classes = stdn_e_clas
* acidemic_plans = acpl_n
* departments = dprt_n
* academic_career = acca_i
* faculty_divisions = dvsn_n

Example output
^^^^^^^^^^^^^^
.. literalinclude:: sample_json/classifications.json
