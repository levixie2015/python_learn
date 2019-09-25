import queue
import threading
import urllib.request
import re
import urllib.error
import requests
from lxml.html import etree
from bs4 import BeautifulSoup

url = 'http://xiaohua.zol.com.cn/lengxiaohua/14.html'

headers = ("User-Agent",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0")
opener = urllib.request.build_opener()
opener.addheaders = [headers]
urllib.request.install_opener(opener)


def parse_detail(data_queue, lock):
    while not data_queue.empty():
        print('正在解析', threading.currentThread().name)

        html = data_queue.get()
        html_element = etree.HTML(html)
        title = html_element.xpath('//h1[@class="article-title"]/text()')

        lock.acquire()  # 加锁
        with open('xiaohua.txt', 'a+', encoding='utf-8') as f:
            f.write(title[0])
            f.write('\n')
        lock.release()


def get_detail(task_queue, data_queue):
    while not task_queue.empty():
        page = task_queue.get()
        print('正在下载第' + str(page) + '页', threading.currentThread().name)
        full_url = 'http://xiaohua.zol.com.cn/lengxiaohua/%s.html' % str(page)
        print(full_url)
        data = urllib.request.urlopen(full_url).read().decode('gbk')
        pat = '<a target="_blank" href="(.*?)" class="all-read"'
        urls = re.compile(pat).findall(data)
        # flag = False
        for url in urls:
            detail_path = 'http://xiaohua.zol.com.cn' + url
            # print(detail_path)
            req_header = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
            response = requests.get(detail_path, headers=req_header)

            if response.status_code == 200:
                # 将获取到的页面源码存到dataQueue队列中
                data_queue.put(response.text)
            else:
                data_queue.put(page)


if __name__ == '__main__':
    list_ = ['lengxiaohua', 'aiqing']
    # 创建任务队列
    task_queue = queue.Queue()
    for i in range(1, 50):
        print(i)
        task_queue.put(i)

    # 创建数据队列
    data_queue = queue.Queue()

    # 创建线程执行下载任务
    threadName = ['下载线程1号', '下载线程2号', '下载线程3号', '下载线程4号']
    crawl_thread = []

    for name in threadName:
        # 创建线程
        thread_crawl = threading.Thread(
            target=get_detail,
            name=name,
            args=(task_queue, data_queue)
        )
        crawl_thread.append(thread_crawl)

        thread_crawl.start()

    # 让所有的爬取线程执行完毕，再回到主线程中继续执行
    for thread in crawl_thread:
        thread.join()

    # 加线程锁

    lock = threading.Lock()

    # 创建解析线程,从dataQueue队列中取出页面源码进行解析
    threadName = ['解析线程1号', '解析线程2号', '解析线程3号', '解析线程4号']
    parse_thread = []
    for name in threadName:
        # 创建线程
        thread_parse = threading.Thread(
            target=parse_detail,
            name=name,
            args=(data_queue, lock)
        )
        parse_thread.append(thread_parse)
        # 开启线程
        thread_parse.start()

    for thread in parse_thread:
        thread.join()

    print('结束了')

