from sgwc import search_articles, Article, get_hot_articles, search_officials, get_official

for article in search_officials('python'):
    print(article)


# for item in get_hot_articles():
#     print(item)
# print(vars(Article()))

# print(get_official('csdn_code'))
# print(r'document\.write\(timeConvert\(\'(.*?)\'\)\)')