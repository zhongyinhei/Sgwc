# Sgwc

## 介绍
搜狗微信文章爬虫

## 安装 
```
pip3 install sgwc
```

## 使用
```
from sgwc import get_official, search_officials, search_articles, get_hot_articles

official = get_official(official_id='official_id')  # 通过微信号查找公众号
officials = search_officials(keyword='keyword')  # 通过关键字查找公众号
articles = search_articles(keyword='keyword')  # 通过关键字查找文章
articles = get_hot_articles()  # 获取热门文章
```

#### Article
#### Official

## API
#### get_official(official_id)
- 返回 `Official` 实例
#### search_officials(keyword, pages=1)
- 返回 `Official` 实例数组
#### search_articles(keyword, pages=1)
- 返回 `Article` 实例数组
#### get_hot_articles(pages=2)
- 

#### Article
###### url --- 链接
###### title --- 标题
###### date --- 日期
###### image_url --- 图片链接
###### digest --- 概述
###### official_url --- 文章公众号链接
###### official_name --- 文章公众号名称
###### save_article(save_path='.') --- 保存文章 Markdown 文件（path：保存路径）

#### Official
###### url --- 链接
###### official_id --- 公众号
###### name --- 公众号名称
###### avatar_url --- 公众号头像链接
###### qr_code_url --- 公众号二维码链接
###### profile_desc --- 公众号简介
###### status
###### recent_article --- 最新文章 Article 实例
###### articles --- 最近文章 Article 实例数组
###### authenticate --- 认证
###### from_url
