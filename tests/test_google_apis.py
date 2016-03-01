from ferrisnose import AppEngineTest
from ferris3 import google_apis
import mock


class GoogleApisTest(AppEngineTest):

    def test_discovery_doc_caching(self):
        http_patch = mock.patch('httplib2.Http.request', return_value=(200, 'test'))
        with http_patch as http:
            doc = google_apis._get_discovery_document('test', 'v1')
            assert doc == 'test'
            assert http.call_count == 1

            doc = google_apis._get_discovery_document('test', 'v1')
            assert doc == 'test'
            assert http.call_count == 1

            doc = google_apis._get_discovery_document('meep', 'v1')
            assert doc == 'test'
            assert http.call_count == 2

    def test_client_caching(self):
        from contextlib import nested

        http_patch = mock.patch('httplib2.Http.request', return_value=(200, 'test'))
        client_patch = mock.patch('apiclient.discovery.build')

        with nested(http_patch, client_patch) as (http, client):
            creds = mock.MagicMock()
            creds.to_json = mock.Mock(return_value="{}")

            google_apis.build("test", "v1", creds)
            assert client.call_count == 1

            google_apis.build("test", "v1", creds)
            assert client.call_count == 1

            google_apis.build("meep", "v1", creds)
            assert client.call_count == 2
