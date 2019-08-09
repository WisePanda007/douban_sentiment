from get_ip import get_ip
from multiprocessing import Pool
if __name__ == '__main__':
    urls=['https://www.xicidaili.com/nn/{}'.format(x) for x in range(128,2000)]
    pool=Pool(4)
    for url in urls:
        pool.apply_async(get_ip().get_ips(url))
    pool.close()
    pool.join()