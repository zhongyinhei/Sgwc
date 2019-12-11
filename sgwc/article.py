from .official import Official
from .utils import parse_link


class Article:
    def __init__(self, **kwargs):
        print(kwargs)
        self._url = kwargs.get('url')
        self._link = kwargs.get('link')
        self.title = kwargs.get('title')
        self.date = kwargs.get('date')
        self.image_url = kwargs.get('image_url')
        self.digest = kwargs.get('digest')
        self._official = kwargs.get('official')
        self._official_url = kwargs.get('official_url')
        self._official_link = kwargs.get('official_link')
        self.official_name = kwargs.get('official_name')

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __str__(self):
        return f'Article(title={self.title}, official_name={self.official_name}, date={self.date})'

    def __repr__(self):
        return f'Article(title={self.title})'

    @property
    def url(self):
        if not self._url:
            if not self._link:
                return None
            self._url = parse_link(self._link)
        return self._url

    @property
    def official(self):
        if not self._official:
            if not self.url:
                return None
            self._official = Official.from_url(self.url)
        return self._official

    @property
    def official_url(self):
        if not self._official_url:
            if not self.official:
                return None
            self._official_url = self.official.url
        return self._official_url

    def save_article(self, save_path='.'):
        pass

    @classmethod
    def from_url(cls, url):
        pass
