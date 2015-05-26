import unittest
import tempfile
import mock
import datetime

import keepaneyeon.versioned

def create_temp_file(contents):
    tmp = tempfile.NamedTemporaryFile()
    tmp.write(contents)
    tmp.flush()
    return tmp


class TestVersionedStorageDigest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = create_temp_file('The quick brown fox jumps over the lazy dog')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.close()

    def test_digest_md5(self):
        """
        VersionedStorage default digest works (md5)
        """
        store = keepaneyeon.versioned.VersionedStorage(store={}, digest='md5')
        digest = store.digest(self.tmp.name)
        self.assertEqual(digest, '9e107d9d372bb6826bd81d3542a419d6')

    def test_digest_sha1(self):
        """
        VersionedStorage sha1 digest works
        """
        store = keepaneyeon.versioned.VersionedStorage(store={}, digest='sha1')
        digest = store.digest(self.tmp.name)
        self.assertEqual(digest, '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12')


class DictStorage():
    """
    Mock storage class to sit behind VersionedStorage for testing
    """
    def __init__(self):
        self.keys = {}

    def exists(self, name):
        return (name in self.keys)

    def store_from_filename(self, name, filename):
        with open(filename, 'rb') as f:
            content = f.read()
        self.store_from_string(name, content)

    def store_from_string(self, name, string):
        self.keys[name] = string


class TestVersionedStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file_initial = create_temp_file('initial')
        cls.file_changed = create_temp_file('changed')

    @classmethod
    def tearDownClass(cls):
        cls.file_initial.close()
        cls.file_changed.close()

    def setUp(self):
        self.store = DictStorage()
        self.versioned = keepaneyeon.versioned.VersionedStorage(self.store)
        datetime_patcher = mock.patch.object(
            keepaneyeon.versioned.datetime, 'datetime',
            mock.Mock(wraps=datetime.datetime)
        )
        self.mocked_datetime = datetime_patcher.start()
        self.mocked_datetime.now.return_value = datetime.datetime(2012, 6, 16)
        self.addCleanup(datetime_patcher.stop)

    def test_store_from_filename(self):
        """
        store_from_filename works
        """
        self.versioned.store_from_filename('test', self.file_initial.name)
        self.assertEqual(self.store.keys, {
            'test/2012-06-16T00:00:00': 'initial',
            '.keepaneyeon/versions/test/cc51b81974287ab79cef9e94fe778cc9':
                'name: test\ntimestamp: 2012-06-16 00:00:00\n',
                })

    def test_changed_store(self):
        """
        stores new version when file has changed
        """
        self.versioned.store_from_filename('test', self.file_initial.name)
        self.mocked_datetime.now.return_value = datetime.datetime(2015, 6, 16)
        self.versioned.store_from_filename('test', self.file_changed.name)
        self.assertEqual(self.store.keys, {
            'test/2012-06-16T00:00:00': 'initial',
            'test/2015-06-16T00:00:00': 'changed',
            '.keepaneyeon/versions/test/cc51b81974287ab79cef9e94fe778cc9':
                'name: test\ntimestamp: 2012-06-16 00:00:00\n',
            '.keepaneyeon/versions/test/8977dfac2f8e04cb96e66882235f5aba':
                'name: test\ntimestamp: 2015-06-16 00:00:00\n',
                })

    def test_repeat_store(self):
        """
        does nothing when the same file is stored again under the same name
        """
        self.versioned.store_from_filename('test', self.file_initial.name)
        self.mocked_datetime.now.return_value = datetime.datetime(2015, 6, 16)
        self.versioned.store_from_filename('test', self.file_initial.name)
        self.assertEqual(self.store.keys, {
            'test/2012-06-16T00:00:00': 'initial',
            '.keepaneyeon/versions/test/cc51b81974287ab79cef9e94fe778cc9':
                'name: test\ntimestamp: 2012-06-16 00:00:00\n',
                })

    def test_same_file_diff_name(self):
        """
        stores same file when stored for a different name
        """
        self.versioned.store_from_filename('test', self.file_initial.name)
        self.versioned.store_from_filename('test2', self.file_initial.name)
        self.assertEqual(self.store.keys, {
            'test/2012-06-16T00:00:00': 'initial',
            '.keepaneyeon/versions/test/cc51b81974287ab79cef9e94fe778cc9':
                'name: test\ntimestamp: 2012-06-16 00:00:00\n',
            'test2/2012-06-16T00:00:00': 'initial',
            '.keepaneyeon/versions/test2/cc51b81974287ab79cef9e94fe778cc9':
                'name: test2\ntimestamp: 2012-06-16 00:00:00\n',
                })
