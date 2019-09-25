import random
import sys

###############获取所有公司名称#########################################
import time

from company import execlUtil, baikeApi2
from company_xin_baidu import xinApi

# excel = execlUtil.excel("C:/Users/xielw/Desktop/公司处理/测试.xlsx")
excel = execlUtil.excel("C:/Users/xielw/Desktop/公司处理/百度企业信用-11480.xlsx")
companyNames = excel.getColValues(1, 1)
total = len(companyNames)
print('companyNames共有[', total, ']条数据')


ips = baikeApi2.getProxyIps()
print(ips)
print("代理ip共有:%s个" %(len(ips)))

while True:
###############获取上次异常的信息#########################################
    with open("exception.txt", 'r', encoding='utf-8') as f:
        beginRow = 0
        rowStr = f.readline()
        if rowStr:
            beginRow = int(rowStr)
            if beginRow == total - 1:
                print("数据已处理完毕!无需处理!")
                break
                # sys.exit()
            print("上次执行异常的行数为【", beginRow, '】行')
        else:
            print("首次执行")
        print("beginRow=", beginRow)

###############遍历所有公司,获取公司信息#########################################
    exceptionRow = 0;
    try:
        list = []
        for i, companyName in enumerate(companyNames[beginRow:]):
            exceptionRow = i + beginRow
            # proxyIp = baikeApi2.getAvailableIp(ips)
            proxyIp = ""
            data = xinApi.parData(companyName, proxyIp)
            print(companyName)
            # print(data)
            list.append(data)
    except Exception as e:
        print(e)
        time.sleep(random.randint(5, 10))
    finally:
        print("异常的行号：[", exceptionRow, ']', '---【', companyName, '】')
        with open("exception.txt", 'w+', encoding='utf-8') as f:
            f.writelines(str(exceptionRow))
        excel.setCellsValue4BaiduXinyong(beginRow, list)
        print('【', beginRow, '】到[', exceptionRow, ']写入数据完毕')
