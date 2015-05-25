import unittest
from mock import patch

from keepaneyeon.fortytwomatters import FortyTwoMattersLookup

class TestFortyTwoMattersLookup(unittest.TestCase):
    @patch('keepaneyeon.http.HttpDownloader')
    def test_download(self, MockHttpDownloader):
        """
        constructs correct 42matters api request
        """
        http_downloader = MockHttpDownloader()
        fortytwo = FortyTwoMattersLookup('token', http_downloader)
        opts = {
                'app': 'com.rovio.angrybirds',
                }
        fortytwo.download(opts, {})
        http_downloader.download.assert_called_once_with(
                {
                    'url': 'https://42matters.com/api/1/apps/lookup.json',
                    'params': {
                        'access_token': 'token',
                        'p': 'com.rovio.angrybirds'
                        }
                    },
                {},
                )
