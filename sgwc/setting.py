from requests import Session


class _Setting:
    def __init__(self):
        self.session = Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36 '
        }
        self.sougo_captcha_callback = _sougo_captcha_callback
        self.wechat_captcha_callback = _wechat_captcha_callback
        self.wechat_link_error_callback = _wechat_link_error_callback
        self.repeat_times = 3
        self.get_proxy = None
        self.proxy_timeout = 10
        self.proxy_error_callback = lambda url: print(f'Proxy error: {url}')


def _sougo_captcha_callback(captcha_image):
    captcha_image.show()
    return input('请输入Sougo验证码：')


def _wechat_captcha_callback(captcha_image):
    captcha_image.show()
    return input('请输入WeChat验证码：')


def _wechat_link_error_callback(url):
    print(f'Link error: {url}')


setting = _Setting()
