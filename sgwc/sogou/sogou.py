from lxml.html import document_fromstring
from sgwc.wechat import Article, Official
from time import localtime, strftime
from sgwc.extract import extract
from .get_html import get_html
from urllib.parse import quote
from json import loads
from re import search
import logging


def search_articles(keyword, page=1):
    search_url = f'https://weixin.sogou.com/weixin?type=2&query={quote(keyword)}&page={page}'
    logging.info('Search article: ' + search_url)
    html_text = get_html(search_url)
    article_nodes = document_fromstring(html_text).xpath('//*[@class="news-list"]/li')
    return [Article(**{
        'link': extract(node, './div[2]/h3/a/@href'),
        'title': extract(node, './div[2]/h3/a', True),
        'date': strftime('%Y-%m-%d', localtime(int(extract(node, './div[2]/div/@t')))),
        'image_url': 'http://' + extract(node, './div[1]/a/img/@src').split('http://')[1],
        'digest': extract(node, './div[2]/p', True),
        'official_link': extract(node, './div[2]/div/a/@href'),
        'official_name': extract(node, './div[2]/div/a', True),
    }) for node in article_nodes]


def search_officials(keyword, page=1):
    search_url = f'https://weixin.sogou.com/weixin?type=1&query={quote(keyword)}&page={page}'
    logging.info('Search official: ' + search_url)
    html_text = get_html(search_url)
    official_nodes = document_fromstring(html_text).xpath('//*[@class="news-box"]/ul/li')
    return [parse_official_node(html_text, node) for node in official_nodes]


def get_official(official_id):
    url = f'https://weixin.sogou.com/weixin?type=1&query={official_id}'
    logging.info('Get official: ' + url)
    html_text = get_html(url)
    official_node = document_fromstring(html_text).xpath('//*[@class="news-box"]/ul/li')
    if official_node:
        official_node = official_node[0]
        if str(official_id) == str(extract(official_node, './div/div[2]/p[2]/label', True)):
            return parse_official_node(html_text, official_node)
    return None


def get_hot_articles(article_type=0, page=1):
    url = f'https://weixin.sogou.com/pcindex/pc/pc_{article_type}/{page}.html'
    logging.info('Get hot article: ' + url)
    html_text = get_html(url)
    article_nodes = document_fromstring(html_text).xpath('/html/body/li')
    return [Article(**{
        'url': extract(node, './div[1]/a/@href'),
        'title': extract(node, './div[2]/h3/a', True),
        'date': strftime('%Y-%m-%d', localtime(int(extract(node, './div[2]/div/span/@t')))),
        'official_url': extract(node, './div[2]/div/a/@href'),
        'official_name': extract(node, './div[2]/div/a', True),
        'digest': extract(node, './div[2]/p', True),
        'image_url': 'https:' + extract(node, './div[1]/a/img/@src'),
    }) for node in article_nodes]


def parse_official_node(html_text, official_node):
    official_node_id = str(official_node.xpath('./@d')[0])
    monthly_data_url = 'https://weixin.sogou.com' + search('var account_anti_url = \"(.*?)\";', html_text)[1]
    monthly_data = loads(get_html(monthly_data_url))['msg']
    status = monthly_data[official_node_id].split(',') if official_node_id in monthly_data else []
    status = (f'月发文: {status[0]}篇', f'月访问: {status[1]}次') if status else ()
    official_id = extract(official_node, './div/div[2]/p[2]/label', True)
    link = extract(official_node, './div/div[2]/p[1]/a/@href')
    name = extract(official_node, './div/div[2]/p[1]/a', True)
    avatar_url = 'https:' + extract(official_node, './div/div[1]/a/img/@src')
    qr_code_url = extract(official_node, './div/div[4]/span/img[1]/@src')
    profile = extract(official_node, './dl[1]/dd', True)
    recent_article = None
    # 获取公众号文章
    dl_nodes = official_node.xpath('./dl[position()>1]')
    for node in dl_nodes:
        dt = extract(node, './dt/text()')
        if dt and '最近文章' in dt:
            article_date = extract(node, './dd/span', True)
            article_date = int(search(r'document\.write\(timeConvert\(\'(.*?)\'\)\)', article_date)[1])
            article_date = strftime('%Y-%m-%d', localtime(article_date))
            recent_article = Article(**{
                'link': extract(node, './dd/a/@href'),
                'title': extract(node, './dd/a', True),
                'date': article_date,
                'official_link': link,
                'official_name': name,
            })
    return Official(**{
        'link': link,
        'id': official_id,
        'name': name,
        'avatar_url': avatar_url,
        'qr_code_url': qr_code_url,
        'profile': profile,
        'status': status,
        'recent_article': recent_article,
    })

