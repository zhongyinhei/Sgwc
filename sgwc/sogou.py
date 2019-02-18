from lxml.html import document_fromstring
from .wechat import Article, Official
from time import localtime, strftime
from requests import Session, utils
from tempfile import TemporaryFile
from json import loads
from PIL import Image
from re import search

_session = Session()


def search_articles(keyword, pages=1):
    search_urls = [f'http://weixin.sogou.com/weixin?type=2&query={keyword}&page={page}' for page in range(1, pages + 1)]
    xpath = '//*[@class="news-list"]/li'
    articles = []
    for search_url in search_urls:
        html_tree = document_fromstring(_get_html(search_url))
        article_nodes = html_tree.xpath(xpath)
        for article_node in article_nodes:
            article_url = str(article_node.xpath('./div[2]/h3/a/@href')[0])
            article_title = str(article_node.xpath('./div[2]/h3/a/text()')[0])
            article_date = strftime('%Y-%m-%d', localtime(int(article_node.xpath('./div[2]/div/@t')[0])))
            article_digest = str(article_node.xpath('./div[2]/p')[0].text_content())
            official_url = str(article_node.xpath('./div[2]/div/a/@href')[0])
            official_name = str(article_node.xpath('./div[2]/div/a/text()')[0])
            articles.append(
                Article(article_url, article_title, article_date, official_url, official_name, article_digest))
    return articles


def search_officials(keyword, pages=1):
    pass


def get_official(official_id):
    search_url = f'http://weixin.sogou.com/weixin?type=1&query={official_id}'
    html_text = _get_html(search_url)
    html_tree = document_fromstring(html_text)
    official_node = html_tree.xpath('//*[@id="main"]/div[4]/ul/li[1]')
    if official_node:
        official_node = official_node[0]
        if str(official_id) == str(official_node.xpath('./div/div[2]/p[2]/label/text()')[0]):
            official_node_id = str(official_node.xpath('./@d')[0])
            monthly_data_url = 'https://weixin.sogou.com' + search('var account_anti_url = \"(.*?)\";', html_text)[1]
            monthly_data = loads(_get_html(monthly_data_url))['msg']
            official_status = monthly_data[official_node_id].split(',')if official_node_id in monthly_data else ()
            official_url = str(official_node.xpath('./div/div[2]/p[1]/a/@href')[0])
            official_name = str(official_node.xpath('./div/div[2]/p[1]/a/text()')[0])
            official_avatar_url = str(official_node.xpath('./div/div[1]/a/img/@src')[0])
            official_qr_code_url = str(official_node.xpath('./div/div[3]/span/img[1]/@src')[0])
            official_profile_desc = str(official_node.xpath('./dl[1]/dd/text()')[0])
            recent_article_url = str(official_node.xpath('./dl[2]/dd/a/@href')[0])
            recent_article_title = str(official_node.xpath('./dl[2]/dd/a/text()')[0])
            recent_article_date = str(official_node.xpath('./dl[2]/dd/span')[0].text_content())
            recent_article_date = int(search('document.write\(timeConvert\(\'(.*?)\'\)\)', recent_article_date)[1])
            recent_article_date = strftime('%Y-%m-%d', localtime(recent_article_date))
            return Official(official_url, official_id, official_name, official_avatar_url, official_qr_code_url,
                            official_profile_desc, official_status, Article(recent_article_url, recent_article_title,
                                                                            recent_article_date, official_url,
                                                                            official_name))
    return None


def _get_html(url):
    resp = _session.get(url)
    if url == resp.url:
        return resp.text
    else:
        cookies = utils.dict_from_cookiejar(_session.cookies)
        snuid = _identify_captcha()
        cookies['SNUID'] = snuid
        cookies['SUV'] = snuid
        _session.cookies = utils.cookiejar_from_dict(cookies)
        return _get_html(url)


def _identify_captcha():
    while True:
        resp = _session.get('http://weixin.sogou.com/antispider/util/seccode.php?tc=100000')
        tf = TemporaryFile()
        tf.write(resp.content)
        captcha_image = Image.open(tf)
        code = _identifying(captcha_image)
        resp = _session.post('https://weixin.sogou.com/antispider/thank.php', data={
            'c': code,
            'r': 'https://weixin.sogou.com/',
            'v': 5
        })
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['code'] == 0:
            print(1)
            return msg['id']
        print('验证码输入错误！')


def _identifying(captcha_image):
    captcha_image.show()
    return input('Sougo验证码：')
