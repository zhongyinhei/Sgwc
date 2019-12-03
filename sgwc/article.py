class Article:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.title = kwargs.get('title')
        self.date = kwargs.get('date')
        self.image_url = kwargs.get('image_url')
        self.digest = kwargs.get('digest')
        self._official = kwargs.get('official')
        self._official_url = kwargs.get('official_url')
        self.official_link = kwargs.get('official_link')
        self.official_name = kwargs.get('official_name')

    def __getitem__(self, key):
        return getattr(self, key, None)

    @property
    def official(self):
        return ''

    @property
    def official_url(self):
        return ''

    def save_article(self, save_path='.'):
        pass

    def _parse_link(self):
        pass

    @classmethod
    def from_url(cls, url):
        pass
