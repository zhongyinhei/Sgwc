# Sgwc

## 介绍
搜狗微信文章爬虫

## 安装 
```
pip3 install sgwc
```

## 使用
```
from sgwc import get_official, search_officials, search_articles

official = get_official(official_id='official_id')  # 通过微信号查找公众号
officials = search_officials(keyword='keyword')  # 通过关键字查找公众号
articles = search_articles(keyword='keyword')  # 通过关键字查找文章
```

## API
#### get_official(official_id)
- 返回 `Official` 实例
#### search_officials(keyword, pages=1)
- 返回 `Official` 实例数组
#### search_articles(keyword, pages=1)
- 返回 `Article` 实例数组

#### Article
###### url
###### title
###### date
###### image_url
###### digest
###### official_url
###### official_name
###### official
###### info
###### save(path='.')

#### Official
###### url
###### official_id
###### name
###### avatar_url
###### qr_code_url
###### profile_desc
###### recent_article
###### articles
###### authenticate
###### monthly_articles
###### monthly_visits
###### info
