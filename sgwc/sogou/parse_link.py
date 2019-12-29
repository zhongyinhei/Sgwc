from requests.structures import CaseInsensitiveDict
from requests import Session
from random import randint
from re import findall
from sgwc.config import sogou_session
from sgwc.sogou.get_html import get_html
import time


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

    # print(sogou_session.cookies)
    # time.sleep(3)
    # sogou_session.get('https://weixin.sogou.com/weixin')
    # sogou_session.headers.update({'Referer': 'https://weixin.sogou.com/weixin'})
    # print(sogou_session.headers)
    # url_fragments = findall(r'url \+= \'(.*?)\';', get_html(url))

    return ''.join(url_fragments).replace('@', '')
