from .official_account import OfficialAccount
from .article import Article
from requests import Session
from lxml import html


class Sgwxer:
    def __init__(self):
        self._session = Session()

    def search_article(self, name, pages=1):
        search_urls = [f'http://weixin.sogou.com/weixin?type=2&query={name}&page={page}' for page in range(1, pages + 1)]
        xpath = '//*[@class="news-list"]/li'
        articles = []
        for search_url in search_urls:
            html_tree = self.get_html(search_url)
            article_nodes = html_tree.xpath(xpath)
            for article_node in article_nodes:
                article_url = article_node.xpath('./div[2]/h3/a/@href')[0]
                official_account_url = article_node.xpath('./div[2]/div/a/@href')[0]
                digest = article_node.xpath('./div[2]/p')[0].text_content()
                articles.append(Article(article_url, official_account_url, digest))
        return articles

    def search_official_account(self, wechat_id):
        search_url = f'http://weixin.sogou.com/weixin?type=1&query={wechat_id}'
        html_tree = self.get_html(search_url)
        xpath = '//*[@id="main"]/div[4]/ul/li[1]/div/div[2]/p[1]/a/@href'
        official_account = html_tree.xpath(xpath)
        if official_account:
            return OfficialAccount(official_account[0])
        else:
            return None

    def get_html(self, url):
        return html.document_fromstring(self._session.get(url).text)
