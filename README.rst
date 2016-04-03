djangorestframework-registration
======================================

|build-status-image| |pypi-version|

Overview
--------

RESTful account registration, activation. This apps is
inspired by django-registration. It uses the same templates as the 
django-registration. 

This package is influenced by the django-registration HMAC workflow.

Registration Endpoint is an rest framework APIView, 
whereas Activation Endpoint is a django TemplateView.


Requirements
------------

-  Python (3.4)
-  Django (1.8, 1.9)
-  Django REST Framework (3.3)

Installation
------------

Install using ``pip``\ …

.. code:: bash

    $ pip install djangorestframework-registration

Example
-------

Include the following urls.

.. code:: python

    urlpatterns = [
        url(r'^api-token-auth/', include('rest_framework_registration.urls')),
    ]

the available resources will be available at ``/api-token-auth/registrations/``
and ``/api-token-auth/activations/<key>``. See the source code for more detail.

Testing
-------

Install testing requirements.

.. code:: bash

    $ pip install -r requirements.txt

Run with runtests.

.. code:: bash

    $ ./runtests.py

You can also use the excellent `tox`_ testing tool to run the tests
against all supported versions of Python and Django. Install tox
globally, and then simply run:

.. code:: bash

    $ tox

Documentation
-------------

To build the documentation, you’ll need to install ``mkdocs``.

.. code:: bash

    $ pip install mkdocs

To preview the documentation:

.. code:: bash

    $ mkdocs serve
    Running at: http://127.0.0.1:8000/

To build the documentation:

.. code:: bash

    $ mkdocs build

.. _tox: http://tox.readthedocs.org/en/latest/

.. |build-status-image| image:: https://secure.travis-ci.org/9gix/django-rest-framework-registration.svg?branch=master
   :target: http://travis-ci.org/9gix/django-rest-framework-registration?branch=master
.. |pypi-version| image:: https://img.shields.io/pypi/v/djangorestframework-registration.svg
   :target: https://pypi.python.org/pypi/djangorestframework-registration
