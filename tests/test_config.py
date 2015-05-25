import unittest
import yaml

import keepaneyeon.config
from keepaneyeon.http import HttpDownloader

class TestConfig(unittest.TestCase):
    def test_register(self):
        # custom type we want to load from YAML
        class A():
            def __init__(self, **opts):
                self.opts = opts
        # YAML loader we will customize
        class CustomLoader(yaml.Loader):
            pass
        # register our new type
        keepaneyeon.config.register(CustomLoader, 'a', A)
        # parse some YAML
        config_string = """
        - !a
          k1: v1
          k2: v2
        """
        parsed = yaml.load(config_string, Loader=CustomLoader)
        self.assertEqual(len(parsed), 1)
        self.assertIsInstance(parsed[0], A)
        self.assertEqual(parsed[0].opts['k1'], 'v1')
        self.assertEqual(parsed[0].opts['k2'], 'v2')

    def test_load(self):
        # test loading one of our registered types
        config_string = """
        - !downloader/http
          k1: v1
          k2: v2
        """
        parsed = keepaneyeon.config.load(config_string)
        self.assertEqual(len(parsed), 1)
        self.assertIsInstance(parsed[0], HttpDownloader)
        self.assertEqual(parsed[0].base['k1'], 'v1')
        self.assertEqual(parsed[0].base['k2'], 'v2')

