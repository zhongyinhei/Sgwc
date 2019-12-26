from requests.structures import CaseInsensitiveDict
from requests import Session
from random import randint
from re import findall


def extract(node, xpath, is_text=False):
    result = node.xpath(xpath)
    if not result:
        return '' if is_text else None
    return result[0].text_content().strip() if is_text else result[0]


def parse_link(link):
    a = link.find('url=')
    b = randint(1, 100)
    c = link[a + b + 25]
    url = f'https://weixin.sogou.com{link}&k={b}&h={c}'
    session = Session()
    session.get('https://weixin.sogou.com/weixin')
    session.headers = CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/66.0.3359.181 Safari/537.36 ',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Referer': 'https://weixin.sogou.com/weixin',
    })
    resp = session.get(url)
    resp.encoding = 'utf-8'
    url_fragments = findall(r'url \+= \'(.*?)\';', resp.text)

    return ''.join(url_fragments).replace('@', '')
