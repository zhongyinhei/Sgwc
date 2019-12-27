from sgwc.config import wechat_session, wechat_captcha_callback
from lxml.html import document_fromstring
from sgwc.extract import extract
from random import randint
import logging


def get_html(url):
    resp = wechat_session.get(url)
    resp.raise_for_status()

    html_node = document_fromstring(resp.text)
    if html_node.xpath('//div[@class="page_verify"]'):
        identify_captcha()
        return get_html(url)

    error_node = html_node.xpath('//h2[@class="weui-msg__title"]')
    if error_node:
        raise Exception(f"WeChat url error: {extract(error_node[0], '.', True)}")

    return str(resp.content, 'utf-8')


def identify_captcha():
    while True:
        cert = randint(100000, 999999)
        resp = wechat_session.get(f'http://mp.weixin.qq.com/mp/verifycode?cert={cert}')
        code = wechat_captcha_callback(resp.content)
        if not code or not isinstance(code, str):
            logging.warning("WeChat 验证码错误!")
            continue
        code = code.strip().lower()
        if code == 'exit':
            raise KeyboardInterrupt

        resp = wechat_session.post('http://mp.weixin.qq.com/mp/verifycode',
                                   data=f'cert={cert}&input={code}&appmsg_token=""')
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['ret'] == 0:
            break
        logging.warning("WeChat 验证码错误!")
