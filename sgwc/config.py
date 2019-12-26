from requests.structures import CaseInsensitiveDict
from tempfile import TemporaryFile
from requests import Session
from PIL import Image


def _sogou_captcha_callback(data):
    """Sougo识别验证码回调函数"""
    tf = TemporaryFile()
    tf.write(data)
    Image.open(tf).show()
    return input('请输入 Sougo 验证码 (输入 exit 退出): ')


def _wechat_captcha_callback(data):
    """WeChat识别验证码回调函数"""
    tf = TemporaryFile()
    tf.write(data)
    Image.open(tf).show()
    return input('请输入 WeChat 验证码 (输入 exit 退出): ')


sogou_captcha_callback = _sogou_captcha_callback
wechat_captcha_callback = _wechat_captcha_callback


# requests.structures.CaseInsensitiveDict
_default_headers = CaseInsensitiveDict({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.181 Safari/537.36 ',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive',
})

# requests.Session
sogou_session = Session()
sogou_session.headers = _default_headers
wechat_session = Session()
wechat_session.headers = _default_headers


