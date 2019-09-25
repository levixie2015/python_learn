from Login.Login import *

## QQ
userName = "*******@qq.com"
password = "******"
url = "https://mail.qq.com/cgi-bin/loginpage"

## 百度
# userName = ""
# password = ""
# url = "https://www.baidu.com/"

def run():
    browser = login(userName, password, url)
    browser.quit()  # 关闭浏览器
if __name__ == '__main__':
    run()
