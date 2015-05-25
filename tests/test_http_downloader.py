import unittest
import StringIO
import requests.exceptions
import responses
import nose.tools

from keepaneyeon.http import HttpDownloader

class TestHttpDownloader(unittest.TestCase):
    def test_build_request_options(self):
        http_downloader = HttpDownloader(a=1, b=2)
        opts = http_downloader.build_request_options({
            'b': 3,
            'stream': 'should be overridden',
            })
        self.assertDictEqual(opts, {
            'method': 'get',
            'a': 1,
            'b': 3,
            'stream': True,
            })

    @responses.activate
    def test_download_success(self):
        url = 'http://example.com/path'
        responses.add(responses.GET, url, body='Hello World!', status=200)
        http_downloader = HttpDownloader()
        out = StringIO.StringIO()
        http_downloader.download({'url': url}, out)
        self.assertEqual(out.getvalue(), 'Hello World!')

    @nose.tools.raises(requests.exceptions.HTTPError)
    @responses.activate
    def test_download_failure(self):
        url = 'http://example.com/path'
        responses.add(responses.GET, url, status=502)
        http_downloader = HttpDownloader()
        out = StringIO.StringIO()
        http_downloader.download({'url': url}, out)
