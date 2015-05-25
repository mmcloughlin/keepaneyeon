import hashlib
import datetime
import yaml

class VersionedStorage():
    def __init__(self, store, digest='md5', meta_directory='.keepaneyeon'):
        self.store = store
        self.digest_type = digest
        self.meta_directory = meta_directory

    def digest(self, filename):
        """
        Return hex digest of the given file. Uses the hash algorithm configured
        with the digest argument to the constructor.
        """
        chunk_size = 1024
        h = getattr(hashlib, self.digest_type)()
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()

    def version_name(self, name, digest):
        return self.meta_directory + '/versions/' + name + '/' + digest

    def store_from_filename(self, name, filename):
        """
        Store given filename under the provided name.
        """
        # check if we already have this version
        digest = self.digest(filename)
        version_name = self.version_name(name, digest)
        if self.store.exists(version_name):
            return
        # this is new
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%dT%H:%M:%S')
        # store the new version
        name_timstamped = name + '/' + ts
        self.store.store_from_filename(name_timstamped, filename)
        # and record the new digest
        metadata = {
                'name': name,
                'timestamp': now,
                }
        metadata_string = yaml.dump(metadata, default_flow_style=False)
        self.store.store_from_string(version_name, metadata_string)
