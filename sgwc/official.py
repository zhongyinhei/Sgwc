class Official:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
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

    @property
    def articles(self):
        return ''

    @classmethod
    def from_url(cls, url):
        pass
