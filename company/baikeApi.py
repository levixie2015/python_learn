from urllib import parse, request
from urllib.request import Request


def parData(companyName):
    url = 'https://baike.baidu.com/wikiui/api/getcertifyinfo?'
    dict1 = {'lemma': companyName}
    url_data = parse.urlencode(dict1)  # unlencode()将字典{k1:v1,k2:v2}转化为k1=v1&k2=v2
    # print(url_data)  # url_data：lemma=%E7%99%BE%E5%BA%A6%E7%BF%BB%E8%AF%91

    data = request.urlopen((url + url_data)).read()  # 读取url响应结果

    data = data.decode('utf-8')  # 将响应结果用utf8编码
    dataDict = eval(data)# 转字典
    dataDict = dataDict['data']
    print("公司信息:",dataDict)

    # print(dataDict['lemmaTitle']) # 公司名称
    # print(dataDict['creditNo']) # 统一社会信用代码
    # print(dataDict['orgCode']) # 组织机构代码
    # print(dataDict['orgRegisterNum']) # 注册号
    # print(dataDict['certStatus']) # 经营状态
    # print(dataDict['level']) # 公司类型
    # print(dataDict['foundTime']) # 成立日期
    # print(dataDict['legalPerson']) # 法定代表人
    # print(dataDict['termTime']) # 营业期限
    # print(dataDict['regCapital']) # 注册资本
    # print(dataDict['checkDate']) # 发照日期
    # print(dataDict['belongOrg']) # 登记机关
    # print(dataDict['location']) # 企业地址
    # print(dataDict['scope']) # 经营范围

    # url_org = parse.unquote(url_data) # 解码url
    # print(url_org)

    companyInfo = {}
    companyInfo['公司名称']=dataDict['lemmaTitle'] # 公司名称
    companyInfo['统一社会信用代码']=dataDict['creditNo'] # 统一社会信用代码
    companyInfo['组织机构代码']=dataDict['orgCode'] # 组织机构代码
    companyInfo['注册号']=dataDict['orgRegisterNum'] # 注册号
    companyInfo['经营状态']=dataDict['certStatus'] # 经营状态
    companyInfo['公司类型']=dataDict['level'] # 公司类型
    companyInfo['成立日期']=dataDict['foundTime'] # 成立日期
    companyInfo['法定代表人']=dataDict['legalPerson'] # 法定代表人
    companyInfo['营业期限']=dataDict['termTime'] # 营业期限
    companyInfo['注册资本']=dataDict['regCapital'] # 注册资本
    companyInfo['发照日期']=dataDict['checkDate'] # 发照日期
    companyInfo['登记机关']=dataDict['belongOrg'] # 登记机关
    companyInfo['企业地址']=dataDict['location'] # 企业地址
    companyInfo['经营范围']=dataDict['scope'] # 经营范围

    # companyInfoList = []
    # companyInfoList.append(dataDict['lemmaTitle']) # 公司名称
    # companyInfoList.append(dataDict['creditNo']) # 统一社会信用代码
    # companyInfoList.append(dataDict['orgCode']) # 组织机构代码
    # companyInfoList.append(dataDict['orgRegisterNum']) # 注册号
    # companyInfoList.append(dataDict['certStatus']) # 经营状态
    # companyInfoList.append(dataDict['level']) # 公司类型
    # companyInfoList.append(dataDict['foundTime']) # 成立日期
    # companyInfoList.append(dataDict['legalPerson']) # 法定代表人
    # companyInfoList.append(dataDict['termTime']) # 营业期限
    # companyInfoList.append(dataDict['regCapital']) # 注册资本
    # companyInfoList.append(dataDict['checkDate']) # 发照日期
    # companyInfoList.append(dataDict['belongOrg']) # 登记机关
    # companyInfoList.append(dataDict['location']) # 企业地址
    # companyInfoList.append(dataDict['scope']) # 经营范围

    print(companyInfo)
    return companyInfo

if __name__ == '__main__':
    # url = "https://baike.baidu.com/wikiui/api/getcertifyinfo?lemma="
    companyName = "山东汇峰装备科技股份有限公司"
    parData(companyName)