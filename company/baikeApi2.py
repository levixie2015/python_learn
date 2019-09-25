import random
from urllib import request, parse

import requests
from company.proxy import checkip
from company.userAgent import getUserAgent


def parData(companyName, proxyIp):
    companyInfo = {}

    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接

    url = 'https://baike.baidu.com/wikiui/api/getcertifyinfo'
    userAgent = getUserAgent()  # 创建动态代理列表，随机选取列表中的用户代理头部信息，伪装请求

    headers = {
        'User-Agent': userAgent,
        'Connection': 'close',
        'Host': 'baike.baidu.com'
    }
    dict = {
        'lemma': companyName
    }
    data = bytes(parse.urlencode(dict), encoding='utf8')

    if proxyIp:
        s.proxies = {"http": "http://" + proxyIp, "https": "http://" + proxyIp}  # 代理ip

    response = s.post(url=url, headers=headers, data=data, timeout=10)

    responseStr = response.content
    # print('responseStr:', responseStr)

    responseDict = eval(responseStr)
    # print('responseDict:', responseDict)

    responseData = responseDict['data']
    # print('responseData:', responseData)

    # 未查到公司信息
    if len(responseData) == 0:
        return companyInfo

    companyInfo['公司名称'] = responseData['lemmaTitle']  # 公司名称
    companyInfo['统一社会信用代码'] = responseData['creditNo']  # 统一社会信用代码
    companyInfo['组织机构代码'] = responseData['orgCode']  # 组织机构代码
    companyInfo['注册号'] = responseData['orgRegisterNum']  # 注册号
    companyInfo['经营状态'] = responseData['certStatus']  # 经营状态
    companyInfo['公司类型'] = responseData['level']  # 公司类型
    companyInfo['成立日期'] = responseData['foundTime']  # 成立日期
    companyInfo['法定代表人'] = responseData['legalPerson']  # 法定代表人
    companyInfo['营业期限'] = responseData['termTime']  # 营业期限
    companyInfo['注册资本'] = responseData['regCapital']  # 注册资本
    companyInfo['发照日期'] = responseData['checkDate']  # 发照日期
    companyInfo['登记机关'] = responseData['belongOrg']  # 登记机关
    companyInfo['企业地址'] = responseData['location']  # 企业地址
    companyInfo['经营范围'] = responseData['scope']  # 经营范围
    # print(companyInfo)
    return companyInfo


def getProxyIps():
    ips = []
    with open('ip.txt', 'r') as f:
        for line in f:
            ips.append(line.strip('\n'))
    return ips


def getAvailableIp(ips):
    value = ""
    ip = random.choice(ips)
    targeturl = 'https://xin.baidu.com'  # 验证ip有效性的指定url
    is_avail = checkip(targeturl, ip)
    if is_avail == True:
        value = ip
    return value


if __name__ == '__main__':
    # 'https: // baike.baidu.com / wikiui / api / getcertifyinfo?lemma =山东汇峰装备科技股份有限公司'
    # companyName = "内蒙古新华建建设集团有限公司"
    # parData(companyName)
    ips = getProxyIps()
    ip = getAvailableIp(ips)
    if not ip:  # 判断输入的用户名或密码是否为空
        print('为空')
