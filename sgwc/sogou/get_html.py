from sgwc.config import sogou_session, sogou_captcha_callback
from requests.utils import add_dict_to_cookiejar
from time import time
import logging


def get_html(url):
    resp = sogou_session.get(url)
    resp.raise_for_status()

    if url != resp.url:
        identify_captcha()
        return get_html(url)
    return str(resp.content, 'utf-8')


def identify_captcha():
    while True:
        sogou_session.headers.update({'Referer': 'https://weixin.sogou.com/antispider/'})
        resp = sogou_session.get(f'http://weixin.sogou.com/antispider/util/seccode.php?tc={int(time())}')
        code = sogou_captcha_callback(resp.content)
        if not code or not isinstance(code, str):
            logging.warning("Sogou 验证码错误!")
            continue
        code = code.strip().lower()
        if code == 'exit':
            raise KeyboardInterrupt
        resp = sogou_session.post('https://weixin.sogou.com/antispider/thank.php', data={
            'c': code,
            'r': 'https://weixin.sogou.com/',
            'v': 5,
        })
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['code'] == 0:
            add_dict_to_cookiejar(sogou_session.cookies, {'SNUID': msg['id']})
            break
        logging.warning("Sogou 验证码错误!")
