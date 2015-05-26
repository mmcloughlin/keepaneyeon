import unittest

from tests.util import DictStorage

from keepaneyeon.target import Target

class StubDownloader():
    def download(self, opts, out):
        out.write(opts['message'])

class TestTarget(unittest.TestCase):
    def test_fetch(self):
        """
        target class links downloader to storage
        """
        store = DictStorage()
        t = Target(
                name='test',
                downloader=StubDownloader(),
                store=store,
                message='Hello World!',
                )
        t.fetch()
        self.assertEqual(store.keys, {'test': 'Hello World!'})
