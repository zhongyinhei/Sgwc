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
###### url --- URL
###### title --- 标题
###### date --- 日期
###### image_url --- 图片URL
###### digest --- 概述
###### official_url --- 文章公众号URL
###### official_name --- 文章公众号名称
###### official --- 文章公众号 Official 实例
###### info --- 文章基本信息（Dict）
###### save(path='.') --- 保存文章 Markdown 文件（path：保存路径）

#### Official
###### url --- URL
###### official_id --- 公众号
###### name --- 公众号名称
###### avatar_url --- 公众号头像URL
###### qr_code_url --- 公众号二维码URL
###### profile_desc --- 公众号简介
###### recent_article --- 最新文章 Article 实例
###### articles --- 最近文章 Article 实例数组
###### authenticate --- 认证
###### monthly_articles --- 月发布文章数
###### monthly_visits --- 月访问量
###### info --- 公众号基本信息（Dict）
