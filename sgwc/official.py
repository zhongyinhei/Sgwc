from lxml.html import document_fromstring
from .utils import parse_link, extract
from .wechat import get_html


class Official:
    def __init__(self, **kwargs):
        self._url = kwargs.get('url')
        self._link = kwargs.get('link')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.avatar_url = kwargs.get('avatar_url')
        self.qr_code_url = kwargs.get('qr_code_url')
        self.profile = kwargs.get('profile')
        self.status = kwargs.get('status')
        self.recent_article = kwargs.get('recent_article')
        self.authenticate = kwargs.get('authenticate')

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __str__(self):
        return f'Official(name={self.name}, id={self.id}, profile={self.profile})'

    def __repr__(self):
        return f'Official(name={self.name}, id={self.id})'

    @property
    def url(self):
        if not self._url and self._link:
            self._url = parse_link(self._link)
        return self._url

    @staticmethod
    def keys():
        return ['url', 'id', 'name', 'avatar_url', 'qr_code_url', 'profile', 'status', 'recent_article',
                'authenticate']

    def values(self):
        return [self[key] for key in self.keys()]

    def items(self):
        return {key: self[key] for key in self.keys()}

    @classmethod
    def from_url(cls, url):
        domain = 'http://mp.weixin.qq.com'
        html_text = get_html(url)
        official_node = document_fromstring(html_text).xpath('//div[@class="page_profile_info"]')[0]
        official_id = extract(official_node, './/p[@class="profile_account"]', True)[5:]
        name = extract(official_node, './/strong[@class="profile_nickname"]', True)
        avatar_url = extract(official_node, './/span[@class="radius_avatar profile_avatar"]/img/@src')
        qr_code_url = domain + extract(official_node, './/img[@id="js_pc_qr_code_img"]/@src')
        profile = extract(official_node, './/ul[@class="profile_desc"]/li[1]/div', True)
        authenticate = extract(official_node, './/ul[@class="profile_desc"]/li[2]/div', True)

        return cls(**{
            'url': url,
            'id': official_id,
            'name': name,
            'avatar_url': avatar_url,
            'qr_code_url': qr_code_url,
            'profile': profile,
            'authenticate': authenticate,
        })
