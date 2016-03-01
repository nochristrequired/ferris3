from __future__ import absolute_import
import httplib2
import logging
import json
import functools
from googleapiclient import discovery, errors
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


def _get_discovery_document(api, api_version, uri_template="https://www.googleapis.com/discovery/v1/apis/{api}/{api_version}/rest", http=None):
    """
    Provides an automatic caching version of the apiclient discovery
    document fetching mechanism using memcache.
    """
    from . import caching
    if not http:
        http = httplib2.Http()

    uri = uri_template.format(api=api, api_version=api_version)

    @caching.cache_using_memcache('gapi-discovery-doc-%s' % uri, 24*60*60)
    def fetch():
        r, c = http.request(uri)
        return r, c

    r, c = fetch()

    return c


def _patch_discovery():
    def patched_build(serviceName, version, http=None, **kwargs):
        doc = _get_discovery_document(serviceName, version, http=http)
        return discovery.build_from_document(doc, http=http, **kwargs)

    setattr(discovery, 'cached_build', patched_build)


_patch_discovery()
