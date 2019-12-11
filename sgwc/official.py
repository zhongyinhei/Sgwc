from .utils import parse_link


class Official:
    def __init__(self, **kwargs):
        print(kwargs)
        self._url = kwargs.get('url')
        self._link = kwargs.get('link')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.avatar_url = kwargs.get('avatar_url')
        self.qr_code_url = kwargs.get('qr_code_url')
        self.profile = kwargs.get('profile')
        self.status = kwargs.get('status')
        self.recent_article = kwargs.get('recent_article')
        self._articles = kwargs.get('articles')
        self.authenticate = kwargs.get('authenticate')

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __str__(self):
        return f'Official(name={self.name}, id={self.id}, profile={self.profile})'

    def __repr__(self):
        return f'Official(name={self.name}, id={self.id})'

    @property
    def url(self):
        if not self._url:
            if not self._link:
                return None
            self._url = parse_link(self._link)
        return self._url

    @property
    def articles(self):
        return ''

    @classmethod
    def from_url(cls, url):
        pass
