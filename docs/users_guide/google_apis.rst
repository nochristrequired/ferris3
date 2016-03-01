Google APIs
===========

.. module:: ferris3.google_apis

Ferris' Google API Helper makes it easy to use Google's recommended `best practices <https://developers.google.com/appengine/articles/efficient_use_of_discovery_based_apis>`_ when interacting with Google APIs via the `Google API Client Library <https://developers.google.com/api-client-library/python/>`_.


Building Clients
----------------

.. autofunction:: build

As demonstrated, valid credentials can be obtained with the help of :mod:`ferris3.oauth2` or with any valid credentials from Google's `oauth2client <https://developers.google.com/api-client-library/python/guide/aaa_oauth>`_.
