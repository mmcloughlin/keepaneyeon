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
