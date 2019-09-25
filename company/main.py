from time import time
import sys
from company import execlUtil, parseData, baikeApi, baikeApi2

# 获取所有公司名称
begin_time = time()
excel = execlUtil.excel("C:/Users/xielw/Desktop/公司处理/对外投资企业名录.xlsx")
# excel = execlUtil.excel("C:/Users/xielw/Desktop/公司处理/测试.xlsx")
companyNames = excel.getColValues(1, 1)
total = len(companyNames)
print('companyNames共有[',total,']条数据')

end_time = time()
run_time = end_time - begin_time
print('该循环程序运行时间：', run_time)  # 该循环程序运行时间： 4.088672876358032

ips = baikeApi2.getProxyIps()
print(ips)
print("代理ip共有:%个", len(ips))

with open("exception.txt", 'r', encoding='utf-8') as f:
    beginRow = 0
    rowStr = f.readline()
    if rowStr:
        beginRow = int(rowStr)
        if beginRow == total - 1:
            print("数据已处理完毕!无需处理!")
            sys.exit()
        print("上次执行异常的行数为【", beginRow, '】行')
    else:
        print("首次执行")
    print("beginRow=",beginRow)

# 爬取数据
begin_time = time()
# url = "https://baike.baidu.com/"
# for companyName in companyNames:

exceptionRow = 0;
try:
    list = []
    for i, companyName in enumerate(companyNames[beginRow:]):
        exceptionRow = i + beginRow
        # print("i=",i,'exceptionRow:',exceptionRow,';companyName=',companyName)
        # data = parseData.parData(url, companyName)
        # proxyIp = baikeApi2.getAvailableIp(ips)
        proxyIp = ""
        data = baikeApi2.parData(companyName, proxyIp)
        print(data)
        list.append(data)
except Exception as e:
    print(e)
else:
    print("else")
finally:
    print(companyName)
    print("异常的行号：", exceptionRow)
    with open("exception.txt", 'w+', encoding='utf-8') as f:
        f.writelines(str(exceptionRow))
    excel.setCellsValue(beginRow,list)
    print('【', beginRow, '】到[', exceptionRow, ']写入数据完毕')

end_time = time()
run_time = end_time - begin_time
print('该循环程序运行时间：', run_time)  # 该循环程序运行时间：
