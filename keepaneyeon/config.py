import yaml

from keepaneyeon.http import HttpDownloader
from keepaneyeon.fortytwomatters import FortyTwoMattersLookup
from keepaneyeon.s3 import S3Storage
from keepaneyeon.versioned import VersionedStorage
from keepaneyeon.target import Target

def register(Loader, tag, cls):
    def constructor(loader, node):
        opts = loader.construct_mapping(node)
        return cls(**opts)
    Loader.add_constructor('!' + tag, constructor)

class YamlLoader(yaml.Loader):
    pass

register(YamlLoader, 'downloader/http', HttpDownloader)
register(YamlLoader, 'downloader/42matters', FortyTwoMattersLookup)
register(YamlLoader, 'storage/s3', S3Storage)
register(YamlLoader, 'storage/versioned', VersionedStorage)
register(YamlLoader, 'target', Target)

def load(stream):
    return yaml.load(stream, Loader=YamlLoader)
