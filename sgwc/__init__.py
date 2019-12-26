from .config import sogou_captcha_callback, wechat_captcha_callback, sogou_session, wechat_session
from .sogou import search_articles, search_officials, get_official, get_hot_articles
from .official import Official
from .article import Article
import importlib
import logging


def set_logging(filepath='', level='INFO'):
    importlib.reload(logging)
    logging.basicConfig(level=level.upper(), filename=filepath, format='%(asctime)s - [%(levelname)s]: %(message)s')


set_logging()
