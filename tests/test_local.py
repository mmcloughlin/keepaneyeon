import unittest
import errno
import tempfile
import shutil
import os.path
import mock
import nose.tools

import keepaneyeon.local

class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.directory = os.path.join(self.tmpdir, 'does/not/exist/yet')
        self.store = keepaneyeon.local.LocalStorage(self.directory)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_exists(self):
        """
        exists returns true for a file we created
        """
        self.store.store_from_string('exists', 'Hello World!')
        self.assertTrue(self.store.exists('exists'))

    def test_does_not_exist(self):
        """
        exists returns false for a file that does not exist
        """
        self.assertFalse(self.store.exists('doesnotexist'))

    def test_store_from_filename(self):
        # create file
        f = tempfile.NamedTemporaryFile()
        f.write('Hello World!')
        f.flush()
        # store it in our store
        self.store.store_from_filename('test', f.name)
        # check it's there
        filename = os.path.join(self.directory, 'test')
        with open(filename, 'rb') as f:
            contents = f.read()
        self.assertEqual(contents, 'Hello World!')

    def test_store_from_string(self):
        self.store.store_from_string('test', 'Hello World!')
        filename = os.path.join(self.directory, 'test')
        with open(filename, 'rb') as f:
            contents = f.read()
        self.assertEqual(contents, 'Hello World!')

    @mock.patch.object(keepaneyeon.local.os.path, 'isdir')
    @mock.patch.object(keepaneyeon.local.os, 'makedirs')
    def test_ensure_directory_errors(self, mock_makedirs, mock_isdir):
        e = OSError('Directory exists')
        e.errno = errno.EEXIST
        mock_makedirs.side_effect = e
        mock_isdir.return_value = True
        self.store.ensure_directory('/tmp/blah/x')

    @nose.tools.raises
    @mock.patch.object(keepaneyeon.local.os, 'makedirs')
    def test_ensure_directory_errors(self, mock_makedirs):
        mock_makedirs.side_effect = Exception('some other error')
        self.store.ensure_directory('/tmp/blah/x')
