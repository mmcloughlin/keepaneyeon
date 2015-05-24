import boto.s3.connection
import boto.s3.key
import urlparse

class S3Storage():
    def __init__(self, **opts):
        self.conn = boto.s3.connection.S3Connection(
                opts['access_key'],
                opts['secret_access_key'])
        components = self.parse_s3_path(opts['path'])
        self.bucket = self.conn.get_bucket(components['bucket'])
        self.base = components['key']

    @staticmethod
    def parse_s3_path(path):
        """
        Parse an S3 URL of the form 's3://bucket/path/to/key'. Returns
        dictionary with keys 'bucket' and 'key'.
        """
        components = urlparse.urlparse(path)
        assert components.scheme == 's3'
        return {
                'bucket': components.netloc,
                'key': components.path,
                }

    def key_for_name(self, name):
        """
        Return full key path for the named file.
        """
        return self.base + '/' + name

    def exists(self, name):
        """
        Determine whether the named file exists.
        """
        k = self.bucket.get_key(self.key_for_name(name))
        return bool(k)

    def store_from_filename(self, name, filename):
        """
        Store given filename under the provided name.
        """
        k = boto.s3.key.Key(self.bucket)
        k.key = self.key_for_name(name)
        k.set_contents_from_filename(filename)

    def store_from_string(self, name, string):
        """
        Store given string under the provided name.
        """
        k = boto.s3.key.Key(self.bucket)
        k.key = self.key_for_name(name)
        k.set_contents_from_string(string)
