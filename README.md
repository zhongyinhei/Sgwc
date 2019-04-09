# Sgwc
搜狗微信文章、公众号爬虫接口。

## 安装 
```
pip3 install sgwc
```

## 使用
```
from sgwc import get_official, search_officials, search_articles, get_hot_articles

official = get_official(official_id='official_id')  # 通过微信号获取指定公众号
officials = search_officials(keyword='keyword')  # 通过关键字搜索公众号
articles = search_articles(keyword='keyword')  # 通过关键字搜索文章
articles = get_hot_articles()  # 获取热门文章
```
#### 从 Article、Official 实例对象提取相关信息
```
article.url
article['url']  # 同时可以像字典类型一样, 提取信息(但不是字典类型)
```
#### 设置验证码回调函数
```
from sgwc import setting

setting.sougo_captcha_callback = sougo_captcha_callback  # 搜狗验证码
setting.wechat_captcha_callback = wechat_captcha_callback  # 微信验证码
```

## API
#### get_official(official_id)
- 返回 `Official` 实例或 `None`
#### search_officials(keyword, pages=1)
- 返回生成 `Official` 实例的 `generator` 对象
#### search_articles(keyword, pages=1)
- 返回生成 `Article` 实例的 `generator` 对象
#### get_hot_articles(pages=2)
- 返回生成 `Article` 实例的 `generator` 对象

#### Article

| 属性 | 返回类型 | 说明 |
|------|:--------:|------|
| url | str | 链接     |
| title | str | 标题     |
| date | str | 日期     |
| image_url | str | 图片链接     |
| digest | str | 概述     |
| official_url | str | 文章公众号链接     |
| official_name | str | 文章公众号名称     |
| save_article(save_path='.') |          | 保存文章 Markdown 文件(save_path: 保存路径)     |
| items() | list | 返回可遍历的(键, 值) 元组数组     |


###### url: str --- 链接
###### title: str --- 标题
###### date: str --- 日期
###### image_url: str --- 图片链接
###### digest: str --- 概述
###### official_url: str --- 文章公众号链接
###### official_name: str --- 文章公众号名称
###### save_article(save_path='.') --- 保存文章 Markdown 文件(save_path: 保存路径)
###### items() --- 返回可遍历的(键, 值) 元组数组

#### Official
###### url: str --- 链接
###### official_id: str --- 公众号
###### name: str --- 公众号名称
###### avatar_url: str --- 公众号头像链接
###### qr_code_url: str --- 公众号二维码链接
###### profile_desc: str --- 公众号简介
###### status: tuple --- 公众号每月状态, (每月发文数, 每月访问数)
###### recent_article: Article --- 最新文章 Article 实例
###### articles: \[Article\] --- 最近文章 Article 实例数组
###### authenticate: str --- 认证
###### from_url(url) --- 类方法, 通过公众号链接生成 Official 实例
###### items() --- 返回可遍历的(键, 值) 元组数组
