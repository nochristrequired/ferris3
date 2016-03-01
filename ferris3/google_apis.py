from __future__ import absolute_import
import httplib2
from googleapiclient import discovery
import hashlib


def build(serviceName, version, credentials):
    """
    Build a Google API client and caches it in the in-process cache. This reduces
    the number of calls to the discovery API as well as making it easy to share
    the client across multiple parts of code with little effort.

    Usage is similar to ``apiclient.discovery.build``, however, instead of passing an http instance
    you just pass in valid credentials and this method will handle constructing an appropriate http instance for you.

    Example::

        credentials = oauth2.build_service_account_credentials(["https://www.googleapis.com/auth/drive"])
        drive = build("drive", "v2", credentials)

    """
    from . import caching
    credentials_hash = hashlib.sha1(credentials.to_json()).hexdigest()
    cache_key = "ferris:google-client-%s-%s-%s" % (serviceName, version, credentials_hash)

    @caching.cache_using_local(cache_key)
    def inner():
        http = httplib2.Http()
        credentials.authorize(http)
        service = discovery.build(serviceName, version, http=http)
        return service

    return inner()
