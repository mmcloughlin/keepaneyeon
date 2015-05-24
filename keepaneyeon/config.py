import yaml

from keepaneyeon.http import HttpDownloader
from keepaneyeon.s3 import S3Storage
from keepaneyeon.versioned import VersionedStorage
from keepaneyeon.target import Target

class YamlLoader(yaml.Loader):
    @classmethod
    def register(self, tag, cls):
        def constructor(loader, node):
            opts = loader.construct_mapping(node)
            return cls(**opts)
        self.add_constructor('!' + tag, constructor)

YamlLoader.register('downloader/http', HttpDownloader)
YamlLoader.register('storage/s3', S3Storage)
YamlLoader.register('storage/versioned', VersionedStorage)
YamlLoader.register('target', Target)

def load(stream):
    return yaml.load(stream, Loader=YamlLoader)
