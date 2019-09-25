import re
import urllib
from urllib import parse

import execjs
import requests

from company.userAgent import getUserAgent2


def mix(tk, baiducode):
    ctx = '''
    function mix(tk, bid){
    tk = tk.split('');var bdLen = bid.length;bid = bid.split('');var one = tk[bid[bdLen - 1]];for(var i = bdLen - 1; i >= 0; i -= 1) {tk[bid[i]] = tk[bid[i - 1]];if ((i - 2) < 0) {tk[bid[i - 1]] = one;break;}}return tk.join("");
    }'''
    # print(tk, baiducode)
    tot = execjs.compile(ctx).call('mix', tk, baiducode)
    # print(tot)
    return tot


def getPidAndTot(company):
    headers = ("User-Agent", getUserAgent2())
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)

    com_decode = parse.quote(company)
    url = 'https://xin.baidu.com/s?q=%s&t=0' % com_decode
    data = urllib.request.urlopen(url).read().decode('utf-8')
    href_path = '<a class="zx-list-item-url" target="_blank" href="(.*?)" title'
    href = re.compile(href_path).findall(data)[0]

    # print("获取href：", href)

    # url = '/detail/compinfo?pid=xlTM-TogKuTwq5GlDjNJdChmos2lFvSZlQmd'
    url = 'https://xin.baidu.com' + str(href)

    # print("url地址：", url)

    ## 获取pid tot
    # print("获取pid and tot开始。。。。。")
    response = requests.get(url)

    rule = re.compile('var tk = document.getElementById\(\'(.*?)\'\).getAttribute\(\'(.*?)\'\);', re.S)
    tk1, tk2 = re.findall(rule, response.text)[0]  # 先从js中获取有tk内容标签的id值和属性名
    rule = re.compile(tk2 + '="(.*?)"')
    tk = re.findall(rule, response.text)[0]  # 从对应标签中获取tk值
    rule = re.compile('id="baiducode">(.*?)<', re.S)
    baiducode = re.findall(rule, response.text)[0]  # 从对应标签中获取baiducode值
    # print("tk:", tk)
    # print("baiducode:", baiducode)
    tot = mix(tk, baiducode)
    # base_url ='https://xin.baidu.com/detail/basicAjax?pid=xlTM-TogKuTwfgCQBQ5sFApAiXFk7RDnQQmd&tot=xlTM-TogKuTw9DRs2Xm05OCTFgTNbCnq1gmd&_=1569301209604'
    base_url = 'https://xin.baidu.com/detail/basicAjax?pid='

    pid = href[21:]
    # basic_url = base_url + pid + "&tot=" + tot

    return pid, tot


if __name__ == '__main__':
    # company = "东莞市全英人力资源有限公司"
    list = ['西双版纳顺源边贸有限公司', '武汉市胭脂物业管理有限责任公司', '山东路通汽车销售服务有限公司', '白山市泰程矿业有限公司']
    for company in list:
        pid, tot = getPidAndTot(company)
        print("pid=", pid, "tot=", tot)
