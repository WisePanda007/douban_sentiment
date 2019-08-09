import requests
import random
class check_ip():
    def __init__(self):
        pass

    def get_headers(self):
        with open('user_agent.txt', 'r') as f:
            users = f.readlines()
            users = [i.rstrip('\n') for i in users]
        return {
            'User-Agent': random.choice(users)}

    def check_ip_douban(self,ip):#检查是否可以登录豆瓣
        print('check...douban...',ip)
        try:
            requests.get('https://movie.douban.com/',headers=self.get_headers(),
                         proxies={'https':ip},timeout=2)
            print('允许访问豆瓣')
            return True
        except Exception as e:
            return False
    def check_ip_xici(self,ip):
        print('check...xici...',ip)
        try:
            requests.get('https://www.xicidaili.com/nt/1/',headers=self.get_headers(),
                         proxies={'https':ip},timeout=2)
            print('允许访问西刺')
            return True
        except Exception as e:
            return False