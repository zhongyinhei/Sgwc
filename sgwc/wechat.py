from .config import wechat_session, wechat_captcha_callback
from random import randint
import logging


# todo: 节点判断
def _get_html(url):
    resp = wechat_session.get(url)
    resp.raise_for_status()

    if '请输入验证码' not in resp.text:
        _identify_captcha()
        return _get_html(url)

    for error_text in ['系统出错', '链接已过期', '该内容已被发布者删除', '此内容因违规无法查看']:
        if error_text in resp.text:
            raise Exception("WeChat url error!")

    return str(resp.content, 'utf-8')


def _identify_captcha():
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
