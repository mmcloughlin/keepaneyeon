import tempfile

class Target():
    def __init__(self, name, downloader, store, **opts):
        self.name = name
        self.downloader = downloader
        self.store = store
        self.opts = opts

    def fetch(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.downloader.download(self.opts, tmp)
            tmp.flush()
            self.store.store_from_filename(self.name, tmp.name)
