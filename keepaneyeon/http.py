import requests

class HttpDownloader():
    def __init__(self, **opts):
        self.base = opts

    def build_request_options(self, opts):
        options = {'method': 'get'}
        options.update(self.base)
        options.update(opts)
        options.update({'stream': True})
        return options

    def download(self, opts, out):
        options = self.build_request_options(opts)
        r = requests.request(**options)
        r.raise_for_status()
        for chunk in r.iter_content(1024):
            out.write(chunk)
