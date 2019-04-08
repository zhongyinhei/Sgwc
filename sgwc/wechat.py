from lxml.html import document_fromstring, tostring
from tempfile import TemporaryFile
from dataclasses import dataclass
from .setting import setting
from requests import Session
from random import randint
from PIL import Image

_session = setting.session


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

    def save_article(self, save_path='.'):
        html_tree = document_fromstring(_get_html(self.url))
        title = self.title
        title = title.replace('/', '-').replace('\\', '-').replace(':', '：').replace('*', '-')
        title = title.replace('"', '”').replace('|', '-').replace('<', '-').replace('>', '-').replace('?', '？')
        with open(f'{save_path}/{title}.md', 'w', encoding='utf-8') as file:
            content_node = html_tree.xpath('//*[@id="js_content"]')[0]
            contents = [tostring(node, encoding='unicode') for node in content_node]
            text = '\n'.join(contents)
            text = text.replace(' data-', ' ')
            file.write(text)


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


def _get_html(url):
    resp = _session.get(url)
    if '请输入验证码' in resp.text:
        _identify_captcha()
        return _get_html(url)
    else:
        resp.encoding = 'utf-8'
        return resp.text


def _identify_captcha():
    while True:
        cert = randint(100000, 999999)
        resp = _session.get(f'http://mp.weixin.qq.com/mp/verifycode?cert={cert}')
        tf = TemporaryFile()
        tf.write(resp.content)
        code = setting.wechat_captcha_callback(Image.open(tf))
        resp = _session.post('http://mp.weixin.qq.com/mp/verifycode', data=f'cert={cert}&input={code}&appmsg_token=""')
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['ret'] == 0:
            break
        print('验证码输入错误！')
