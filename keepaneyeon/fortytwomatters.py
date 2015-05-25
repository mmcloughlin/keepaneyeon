class FortyTwoMattersLookup():
    """
    Download Android app metadata from 42matters API.
    Documentation: https://42matters.com/api/lookup
    """

    url = 'https://42matters.com/api/1/apps/lookup.json'

    def __init__(self, access_token, http_downloader, **opts):
        self.base = opts
        self.base.update({
            'access_token': access_token,
            })
        self.http_downloader = http_downloader

    def download(self, opts, out):
        params = {}
        params.update(self.base)
        params.update(opts)
        params['p'] = params['app']
        del params['app']
        options = {
                'url': self.url,
                'params': params,
                }
        return self.http_downloader.download(options, out)
