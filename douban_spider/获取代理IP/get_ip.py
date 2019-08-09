import requests
import re
from check_ip import check_ip
import random
import time

class get_ip():
    def __init__(self):
        self.usable_http=[]
        self.usable_https=[]

    def get_headers(self):
        with open('user_agent.txt', 'r') as f:
            users = f.readlines()
            users = [i.rstrip('\n') for i in users]
        return {
            'User-Agent': random.choice(users)}

    def get_proxies(self):
        with open('ips/xici_https.txt', 'r') as f:
            https = f.readlines()
            https = [i.rstrip('\n') for i in https]
        return {'https': random.choice(https)}

    def get_ips(self,url):
        print(url)
        try:
            html = requests.get(url, headers=self.get_headers(),timeout=1)
        except:
            return self.get_ips(url)
        res = re.findall(r'alt="Cn" /></td>(.*?)<div', html.text, re.S)
        for i in res:
            ips = re.findall('<td>(.*?)</td>', i)
            ip, port, htt = ips[0], ips[1], ips[2]
            ipport=ip+':'+port
            #print(ipport,htt)#打印所爬取到的ip
            if htt == 'HTTP':
                http=open('ips/未确认http.txt','a+')
                http.write(ipport)
                http.write('\n')
                http.close()
            if htt == 'HTTPS':
                https=open('ips/未确认https.txt','a+')
                https.write(ipport)
                https.write('\n')
                https.close()
                if check_ip().check_ip_douban(ipport):
                    https =open('ips/douban_https.txt', 'a+')
                    https.write(ipport)
                    https.write('\n')
                    https.close()
                if check_ip().check_ip_xici(ipport):
                    https =open('ips/xici_https.txt', 'a+')
                    https.write(ip)
                    https.write('\n')
                    https.close()
                    self.usable_https.append(ipport)