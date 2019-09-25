import json
import random
import re
import time
import urllib
from urllib import request, parse
from urllib.request import ProxyHandler, build_opener

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
    basic_url = base_url + pid + "&tot=" + tot

    return pid, tot

def parData(company, proxyIp):

    companyInfo = {}

    pid, tot = getPidAndTot(company)

    url = 'https://xin.baidu.com/detail/basicAjax?'
    dict = {
        'pid': pid,
        'tot': tot,
        '_': int(round(time.time() * 1000))
    }

    headers = ("User-Agent",getUserAgent2())
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    ##########################################################################################
    # 创建一个IP代理对象
    if proxyIp:
        proxies = {"http": "http://" + proxyIp, "https": "http://" + proxyIp}  # 代理ip
        proxy_handler = ProxyHandler(proxies)
        # 根据IP代理对象，创建用于发送请求的opener对象
        opener = build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    ##########################################################################################

    url_data = parse.urlencode(dict)  # unlencode()将字典{k1:v1,k2:v2}转化为k1=v1&k2=v2
    # print(url_data)  # url_data：lemma=%E7%99%BE%E5%BA%A6%E7%BF%BB%E8%AF%91
    data = request.urlopen((url + url_data)).read()  # 读取url响应结果

    # 未查到公司信息
    if len(data) == 0:
        return companyInfo

    data = data.decode('utf-8')  # 将响应结果用utf8编码
    jsonData = json.loads(data)
    dataDict = jsonData['data']

    companyInfo['公司名称'] = dataDict['entName']  # 公司名称
    companyInfo['统一社会信用代码']=dataDict['unifiedCode'] # 统一社会信用代码
    companyInfo['组织机构代码']=dataDict['orgNo'] # 组织机构代码
    companyInfo['工商注册号']=dataDict['licenseNumber'] # 工商注册号
    companyInfo['经营状态']=dataDict['openStatus'] # 经营状态
    companyInfo['企业类型']=dataDict['entType'] # 企业类型
    companyInfo['成立日期']=dataDict['startDate'] # 成立日期
    companyInfo['法定代表人']=dataDict['legalPerson'] # 法定代表人
    companyInfo['营业期限']=dataDict['openTime'] # 营业期限
    companyInfo['注册资本']=dataDict['regCapital'] # 注册资本
    companyInfo['注册地址']=dataDict['regAddr'] # 注册地址
    companyInfo['登记机关']=dataDict['authority'] # 登记机关
    companyInfo['经营范围']=dataDict['scope'] # 经营范围

    return companyInfo

if __name__ == '__main__':
    # company = "东莞市全英人力资源有限公司"
    list = ['西双版纳顺源边贸有限公司','武汉市胭脂物业管理有限责任公司','山东路通汽车销售服务有限公司','白山市泰程矿业有限公司']
    for i in list:
        companyInfo = parData(i, "")
        print(companyInfo)