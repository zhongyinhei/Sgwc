from lxml.html import document_fromstring, tostring
from tempfile import TemporaryFile
from dataclasses import dataclass
from requests import Session
from random import randint
from PIL import Image

_session = Session()
_session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 '
}


@dataclass(frozen=True)
class Article:
    url: str
    title: str
    date: str
    official_url: str
    official_name: str
    digest: str = None
    image_url: str = None

    def __getitem__(self, key):
        return getattr(self, key, None)

    def items(self):
        return [(key, value) for key, value in vars(self).items()]

    def save_article(self):
        pass


@dataclass(frozen=True)
class Official:
    url: str
    official_id: str
    name: str
    avatar_url: str
    qr_code_url: str
    profile_desc: str
    status: tuple
    recent_article: Article = None
    articles: [Article] = None
    authenticate: str = None

    def __getitem__(self, key):
        return getattr(self, key, None)

    @classmethod
    def from_url(cls):
        pass

    def items(self):
        return [(key, value) for key, value in vars(self).items()]


def _identify_captcha():
    while True:
        cert = randint(100000, 999999)
        resp = _session.get(f'http://mp.weixin.qq.com/mp/verifycode?cert={cert}')
        tf = TemporaryFile()
        tf.write(resp.content)
        captcha_image = Image.open(tf)
        code = _identifying(captcha_image)
        resp = _session.post('http://mp.weixin.qq.com/mp/verifycode', data=f'cert={cert}&input={code}&appmsg_token=""')
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['ret'] == 0:
            break
        print('验证码输入错误！')


def _identifying(captcha_image):
    captcha_image.show()
    return input('请输入WeChat验证码：')
