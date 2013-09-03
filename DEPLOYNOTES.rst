.. _DEPLOYNOTES:

DEPLOYNOTES
===========

Initial setup
-------------

* Install python dependencies (virtualenv is recommended)::

  pip install -r pip-install-req.txt

* Copy ``libraryuse/localsettings.py.dist`` to ``libraryuse/localsettings.py``
  and customize as needed.

* Initialize the database::

  python manage.py syncdb
  python manage.py dbops --refresh-esd
  python manage.py dbops --refresh-libraryvisit



