import pymongo
# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
db = client['douban']
table = db['movie_items']
data=table.find({},{'_id':0,'id':1} )
ids=[i['id'] for i in data]

import random
def get_headers():
    with open('user_agent.txt','r') as f:
        users=f.readlines()
        users=[i.rstrip('\n') for i in users]
    return{'User-Agent':random.choice(users)}
def get_proxies():
    with open('final_douban_https.txt','r') as f:
        https=f.readlines()
        https=[i.rstrip('\n') for i in https]
    return{'https':random.choice(https)}
def get_cookies():
    cookie='bid=hVBCSRNPRjQ; douban-fav-remind=1; gr_user_id=6dd3c308-8536-4566-bce3-4e605c205df8; _vwo_uuid_v2=D2D6CC396CCCA1406E1277D5C515963B2|cf08af69025f901fc58b9d4c33bcfb81; ll="108288"; __yadk_uid=V2tg6WiXtdYv5yAgKCibK1ucFpFU1woR; push_noty_num=0; push_doumail_num=0; __gads=ID=0d6684e69bdb55d4:T=1556710974:S=ALNI_MZM0d22XSAtRv6bwAgIDVH1Uw2F0w; viewed="30471284_25862578_10607365_27180929_30173624_30236842_26977414_30275915"; ct=y; __utmv=30149280.19596; ps=y; __utmc=30149280; __utmc=223695111; __utma=30149280.1352673927.1556942686.1557060678.1557108936.7; __utmz=30149280.1557108936.7.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1557108937%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.969100824.1556547778.1557060678.1557108937.13; __utmb=223695111.0.10.1557108937; __utmz=223695111.1557108937.13.8.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt_douban=1; __utmt=1; __utmb=30149280.5.10.1557108936; _pk_id.100001.4cf6=5d08a517ff50e27f.1556547777.13.1557110472.1557060678.'
    cookie_dict = {i.split("=")[0]:i.split("=")[-1] for i in cookie.split("; ")}
    return cookie_dict


import requests
from lxml import etree
import pymongo
import random
from multiprocessing import Pool
from dns_cache import _setDNSCache

client = pymongo.MongoClient('localhost', 27017)  # 连接数据库
douban = client['douban']  # 创建新数据库
movie_comments = douban['movie_comments']  # 创建数据集合
insert_num = 0


def get_comment_url(idcard):  # 获取每部电影短评的链接
    raw_url = 'https://movie.douban.com/subject/' + idcard + '/comments?start={}&limit=20&sort=new_score&status=P'
    urls = [raw_url.format(x) for x in range(0, 220, 20)]
    for url in urls:
        get_comment_info(url)


def get_comment_info(url):  # 获取电影详细信息
    print(url)
    _setDNSCache()
    try:
        proxy = get_proxies()
        html = requests.get(url, headers=get_headers(), cookies=get_cookies(), proxies=proxy, timeout=1)
    except:
        print(proxy, '异常')
        return get_comment_info(url)

    response = etree.HTML(html.text)
    if response.xpath('//div[@class="comment-item"]') == []:
        print(proxy, '可以登录，IP受限')
        return get_comment_info(url)

    for item in response.xpath('//div[@class="comment-item"]'):
        comment = {}
        try:
            # 电影唯一id
            comment['movie_id'] = response.xpath('//div[@class="fright"]/a/@name')[0].split('-')[-1]
            # 短评的唯一id
            comment['comment_id'] = int(
                item.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/input/@value')[0].strip())
            # 多少人评论有用
            comment['useful_num'] = item.xpath('div[@class="comment"]/h3/span[@class="comment-vote"]/span/text()')[
                0].strip()
            # 评分
            comment['star'] = item.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[2]/@class')[
                0].strip()
            # 评论时间
            comment['time'] = \
            item.xpath('div[@class="comment"]/h3/span[@class="comment-info"]/span[@class="comment-time "]/text()')[
                0].strip()
            # 评论内容
            comment['content'] = item.xpath('div[@class="comment"]/p/span/text()')[0].strip()
            # 评论者名字（唯一）
            comment['people'] = item.xpath('div[@class="avatar"]/a/@title')[0].strip()
            # 评论者页面
            comment['people_url'] = item.xpath('div[@class="avatar"]/a/@href')[0].strip()

            global insert_num
            insert_num += 1
            print('第', insert_num, '次插入数据')
            movie_comments.insert_one(comment)
            print(comment)
        except IndexError:
            print(url, ':发生IndexError')
            pass


if __name__ == '__main__':
    pool = Pool(4)
    for i in ids:
        pool.apply_async(get_comment_url(i))
    pool.close()
    pool.join()