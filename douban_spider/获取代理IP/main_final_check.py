import requests
from lxml import etree
import random

def get_headers():
    with open('user_agent.txt','r') as f:
        users=f.readlines()
        users=[i.rstrip('\n') for i in users]
    return{'User-Agent':random.choice(users)}

def check_ip_douban(ip):#检查是否可以登录豆瓣
    print('check...douban...',ip)
    try:
        a=20*random.randint(0,10)
        url='https://movie.douban.com/subject/26100958/comments?start={}&limit=20&sort=new_score&status=P'.format(a)
        print(url)
        html=requests.get(url,headers=get_headers(),
                     proxies={'https':ip},timeout=2)
        response=etree.HTML(html.text)
        # if response.xpath('//div[@class="comment-item"]')==[]:
        #     print(ip,'异常')
        #     return False
        print(ip,'允许访问豆瓣')
        with open('final_douban_https.txt','a+') as f:
            f.write(ip)
            f.write('\n')
    except Exception as e:
        print(ip, '异常')
        return False


if __name__=='__main__':
    with open('ips/douban_https.txt','r') as f:
        https=f.readlines()
        https=[i.rstrip('\n') for i in https]
    for ip in https:
        check_ip_douban(ip)