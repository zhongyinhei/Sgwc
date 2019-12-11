from requests.structures import CaseInsensitiveDict
from requests import Session
import logging


def _sougo_captcha_callback(data):
    """Sougo识别验证码回调函数"""
    pass


def _wechat_captcha_callback(data):
    """WeChat识别验证码回调函数"""
    pass


def _wechat_link_failure_callback(url):
    """WeChat链接失效回调函数"""
    logging.warning(f"Link failure: {url}.")


sougo_captcha_callback = _sougo_captcha_callback
wechat_captcha_callback = _wechat_captcha_callback
wechat_link_error_callback = _wechat_link_failure_callback
log_file_path = ''


# requests.structures.CaseInsensitiveDict
_default_headers = CaseInsensitiveDict({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 ',
    'Accept-Encoding': ', '.join(('gzip', 'deflate')),
    'Accept': '*/*',
    'Connection': 'keep-alive',
})

# requests.Session
sogou_session = Session()
sogou_session.headers = _default_headers
wechat_session = Session()
wechat_session.headers = _default_headers


