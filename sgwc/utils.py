from .config import sogou_session
from random import randint
from re import findall


def extract(node, xpath, is_text=False):
    result = node.xpath(xpath)
    if not result:
        return None
    if is_text:
        return result[0].text_content().strip()
    return result[0]


# todo: 是否需要验证码
def parse_link(link):
    a = link.find('url=')
    b = randint(1, 100)
    c = link[a + b + 30]
    url = f'https://weixin.sogou.com{link}&k={b}&h={c}'
    resp = sogou_session.get(url)
    resp.encoding = 'utf-8'
    url_fragments = findall(r'url \+= \'(.*?)\';', resp.text)
    return ''.join(url_fragments).replace('@', '')
