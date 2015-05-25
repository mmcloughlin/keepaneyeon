import unittest
import boto
import moto
import tempfile

import keepaneyeon.s3

class TestS3Storage(unittest.TestCase):
    def setUp(self):
        self.mock = moto.mock_s3()
        self.mock.start()
        conn = boto.connect_s3()
        self.bucket = conn.create_bucket('bucket')
        self.store = keepaneyeon.s3.S3Storage(
                access_key='access', secret_access_key='secret',
                path='s3://bucket/path/to')

    def tearDown(self):
        self.mock.stop()

    def test_parse_s3_path(self):
        """
        parses s3 scheme URLs correctly
        """
        parsed = self.store.parse_s3_path('s3://buck/p/t/k')
        self.assertEqual(parsed['bucket'], 'buck')
        self.assertEqual(parsed['key'], '/p/t/k')

    def test_exists_case_false(self):
        """
        exists() returns false for a non-existant key
        """
        res = self.store.exists('test')
        self.assertFalse(res, 'key should not exist')

    def test_exists_case_true(self):
        """
        exists() returns false for an existing key
        """
        k = boto.s3.key.Key(self.bucket)
        k.key = '/path/to/test'
        k.set_contents_from_string('exists')
        res = self.store.exists('test')
        self.assertTrue(res, 'key should exist')

    def test_store_from_filename(self):
        """
        stores data from filename
        """
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write('Hello World!')
            tmp.flush()
            self.store.store_from_filename('test', tmp.name)
        k = self.bucket.get_key('/path/to/test')
        self.assertTrue(k)
        data = k.get_contents_as_string()
        self.assertEqual(data, 'Hello World!')

    def test_store_from_string(self):
        """
        stores data from string
        """
        self.store.store_from_string('test', 'Hello World!')
        k = self.bucket.get_key('/path/to/test')
        self.assertTrue(k)
        data = k.get_contents_as_string()
        self.assertEqual(data, 'Hello World!')
