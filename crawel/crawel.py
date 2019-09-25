# coding=utf-8
import requests,csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from lxml import etree #lxml最新版本没有etree功能，3.7.2有，使用：pip install lxml==3.7.2

def csv_w(fileName,content):
    '用于csv格式文件，写入数据。数据用列表形式'
    #打开文件，追加
    file = open(fileName,'a',newline="")
    #设定写入模式
    csv_write = csv.writer(file,dialect='excel')
    #写入具体的内容
    csv_write.writerow(content)
    file.close()

def save(fileName,title): # 爬取双色球历史数据，写入到csv文件中
    csv_w(fileName, title)  # 表头

    url = "http://datachart.500.com/ssq/history/newinc/history.php?start=00001&end=19094" #数据来源
    response = requests.get(url)
    response = response.text
    selector = etree.HTML(response)
    trs = selector.xpath('//tr[@class="t_tr1"]')
    for tr in reversed(trs):
        id = tr.xpath('td/text()')[0]
        reds = tr.xpath("td/text()")[1:7]
        blue = tr.xpath("td/text()")[7]
        date = tr.xpath("td/text()")[-1]
        resultList = []
        # resultList.append(id)
        resultList.append(blue)
        for red in reds:
            resultList.append(red)
        # resultList.append(date)
        csv_w(fileName,resultList) # 数据
if __name__ == '__main__':
    # title=['id','blue','red_one','red_two','red_three','red_four','red_five','red_six','date']
    title=['blue','red_one','red_two','red_three','red_four','red_five','red_six']
    save("data2.csv",title)
    print("wirte over")
