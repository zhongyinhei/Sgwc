from sgwc.sogou.parse_link import parse_link
from lxml.html import document_fromstring
from sgwc.extract import extract
from .get_html import get_html
from re import search


class Article:
    def __init__(self, **kwargs):
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
        self._html = kwargs.get('html')

    def __getitem__(self, key):
        return getattr(self, key, None)

    def __str__(self):
        return f'Article(title={self.title}, official_name={self.official_name}, date={self.date})'

    def __repr__(self):
        return f'Article(title={self.title})'

    @property
    def url(self):
        if not self._url and self._link:
            self._url = parse_link(self._link)
        return self._url

    @property
    def official(self):
        if not self._official and self.official_url:
            self._official = Official.from_url(self.official_url)
        return self._official

    @property
    def official_url(self):
        if not self._official_url:
            if self._official:
                self._official_url = self._official.url
            elif self._official_link:
                self._official_url = parse_link(self._official_link)
        return self._official_url

    @property
    def html(self):
        if not self._html and self.url:
            self._html = get_html(self.url)
        return self._html

    @staticmethod
    def keys():
        return ['url', 'title', 'date', 'image_url', 'digest', 'official', 'official_url', 'official_name']

    def values(self):
        return [self[key] for key in self.keys()]

    def items(self):
        return {key: self[key] for key in self.keys()}

    @classmethod
    def from_url(cls, url):
        domain = 'http://mp.weixin.qq.com'
        html_text = get_html(url)
        article_node = document_fromstring(html_text).xpath('//div[@id="js_article"]')[0]
        title = extract(article_node, './/h2[@id="activity-name"]', True)
        date = search('",s="(.*?)"', html_text)[1]
        image_url = search('var msg_cdn_url = "(.*?)";', html_text)[1]
        digest = extract(article_node, './/div[@id="js_content"]', True)[:100] + '...'

        official_name = extract(article_node, './/strong[@class="profile_nickname"]', True)
        official_avatar_url = search('var round_head_img = "(.*?)";', html_text)[1]
        official_qr_code_url = domain + search('window.sg_qr_code="(.*?)";', html_text)[1].replace(r'\x26amp;', '&')
        official_id = extract(article_node, './/p[@class="profile_meta"][1]/span', True)
        official_profile = extract(article_node, './/p[@class="profile_meta"][2]/span', True)
        official = Official(**{
            'id': official_id,
            'name': official_name,
            'avatar_url': official_avatar_url,
            'qr_code_url': official_qr_code_url,
            'profile': official_profile,
        })

        return cls(**{
            'url': url,
            'title': title,
            'date': date,
            'image_url': image_url,
            'digest': digest,
            'official': official,
            'official_name': official_name,
            'html': html_text,
        })



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
