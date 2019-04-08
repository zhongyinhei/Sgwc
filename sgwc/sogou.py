from requests.utils import add_dict_to_cookiejar
from lxml.html import document_fromstring
from .wechat import Article, Official
from time import localtime, strftime
from tempfile import TemporaryFile
from re import search, findall
from .setting import setting
from random import randint
from json import loads
from time import time
from PIL import Image

_session = setting.session


def search_articles(keyword, pages=1):
    search_urls = [f'http://weixin.sogou.com/weixin?type=2&query={keyword}&page={page}' for page in range(1, pages + 1)]
    for search_url in search_urls:
        article_nodes = document_fromstring(_get_html(search_url)).xpath('//*[@class="news-list"]/li')
        _session.headers.update({'Referer': search_url})
        for node in article_nodes:
            yield Article(
                url=_extract(node, './div[2]/h3/a/@data-share'),
                title=_extract(node, './div[2]/h3/a', True),
                date=strftime('%Y-%m-%d', localtime(int(_extract(node, './div[2]/div/@t')))),
                image_url=_extract(node, './div[1]/a/img/@src'),
                digest=_extract(node, './div[2]/p', True),
                official_url=_parse_link(_extract(node, './div[2]/div/a/@href')),
                official_name=_extract(node, './div[2]/div/a/text()'),
            )


def search_officials(keyword, pages=1):
    search_urls = [f'http://weixin.sogou.com/weixin?type=1&query={keyword}&page={page}' for page in range(1, pages + 1)]
    for search_url in search_urls:
        _session.headers.update({'Referer': search_url})
        html_text = _get_html(search_url)
        html_tree = document_fromstring(html_text)
        official_nodes = html_tree.xpath('//*[@id="main"]/div[4]/ul/li')
        for official_node in official_nodes:
            yield _parse_official_node(html_text, official_node)


def get_official(official_id):
    search_url = f'http://weixin.sogou.com/weixin?type=1&query={official_id}'
    _session.headers.update({'Referer': search_url})
    html_text = _get_html(search_url)
    html_tree = document_fromstring(html_text)
    official_node = html_tree.xpath('//*[@id="main"]/div[4]/ul/li[1]')
    if official_node:
        official_node = official_node[0]
        if str(official_id) == str(_extract(official_node, './div/div[2]/p[2]/label/text()')):
            return _parse_official_node(html_text, official_node)
    return None


def get_hot_articles(pages=2):
    urls = [f'https://weixin.sogou.com/pcindex/pc/pc_0/{index}.html' for index in range(1, pages + 1)]
    for url in urls:
        html_tree = document_fromstring(_get_html(url))
        article_nodes = html_tree.xpath('/html/body/li')
        for node in article_nodes:
            url = _extract(node, './div[1]/a/@href')
            title = _extract(node, './div[2]/h3/a', True)
            date = _extract(node, './div[2]/div/span/@t')
            date = strftime('%Y-%m-%d', localtime(int(date)))
            official_url = _extract(node, './div[2]/div/a/@href')
            official_name = _extract(node, './div[2]/div/a', True)
            digest = _extract(node, './div[2]/p', True)
            image_url = _extract(node, './div[1]/a/img/@src')
            yield Article(url, title, date, official_url, official_name, digest, image_url)


def _parse_official_node(html_text, official_node):
    official_node_id = str(official_node.xpath('./@d')[0])
    monthly_data_url = 'https://weixin.sogou.com' + search('var account_anti_url = \"(.*?)\";', html_text)[1]
    monthly_data = loads(_get_html(monthly_data_url))['msg']
    status = monthly_data[official_node_id].split(',') if official_node_id in monthly_data else []
    status = (f'月发文: {status[0]}篇', f'月访问: {status[1]}次') if status else ()
    official_id = _extract(official_node, './div/div[2]/p[2]/label/text()')
    url = _parse_link(_extract(official_node, './div/div[2]/p[1]/a/@href'))
    name = _extract(official_node, './div/div[2]/p[1]/a', True)
    avatar_url = _extract(official_node, './div/div[1]/a/img/@src')
    qr_code_url = _extract(official_node, './div/div[3]/span/img[1]/@src')
    profile_desc = _extract(official_node, './dl[1]/dd', True)
    recent_article = None

    dl_nodes = official_node.xpath('./dl[position()>1]')
    for node in dl_nodes:
        dt = _extract(node, './dt/text()')
        if dt and '最近文章' in dt:
            article_date = _extract(node, './dd/span', True)
            article_date = int(search('document.write\(timeConvert\(\'(.*?)\'\)\)', article_date)[1])
            article_date = strftime('%Y-%m-%d', localtime(article_date))
            recent_article = Article(
                url=_parse_link(_extract(node, './dd/a/@href')),
                title=_extract(node, './dd/a', True),
                date=article_date,
                official_url=url,
                official_name=name,
            )
    return Official(url, official_id, name, avatar_url, qr_code_url, profile_desc, status, recent_article)


def _get_html(url):
    resp = _session.get(url)
    if url == resp.url:
        resp.encoding = 'utf-8'
        return resp.text
    else:
        snuid = _identify_captcha()
        add_dict_to_cookiejar(_session.cookies, {'SNUID': snuid, 'SUV': snuid})
        return _get_html(url)


def _extract(node, xpath, is_text=False):
    result = node.xpath(xpath)
    result = result[0] if result else None
    return None if result is None else result.text_content().strip() if is_text else result


def _parse_link(link):
    if not link or'&k' in link:
        return link
    else:
        b = randint(1, 100)
        a = link.find('url=')
        c = link[a + b + 30]
        url = f'https://weixin.sogou.com{link}&k={b}&h={c}'
        resp = _session.get(url)
        resp.encoding = 'utf-8'
        url_fragments = findall('url \+= \'(.*?)\';', resp.text)
        return ''.join(url_fragments).replace('@', '')


def _identify_captcha():
    while True:
        resp = _session.get(f'http://weixin.sogou.com/antispider/util/seccode.php?tc={int(time())}')
        tf = TemporaryFile()
        tf.write(resp.content)
        code = setting.sougo_captcha_callback(Image.open(tf))
        resp = _session.post('https://weixin.sogou.com/antispider/thank.php', data={
            'c': code,
            'r': 'https://weixin.sogou.com/',
            'v': 5
        })
        resp.encoding = 'utf-8'
        msg = resp.json()
        if msg['code'] == 0:
            return msg['id']
        print('验证码输入错误！')
