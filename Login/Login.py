from time import sleep
from selenium import webdriver

def login(userName, password, url):
    # 创建chrome参数对象
    opt = webdriver.ChromeOptions()
    # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
    opt.set_headless()
    # 创建chrome无界面对象
    driver = webdriver.Chrome(options=opt)

    driver.get(url)
    print(driver.title)

    ### QQ邮箱
    sleep(3)
    driver.switch_to.frame('login_frame')
    driver.find_element_by_xpath('//a[@class="switch_btn"]').click()
    driver.find_element_by_id("u").send_keys(userName)
    driver.find_element_by_id("p").send_keys(password)
    driver.find_element_by_id("login_button").click()
    driver.maximize_window()

    ### 百度
    # sleep(3)
    # driver.find_element_by_id("TANGRAM__PSP_10__footerULoginBtn").click()
    # driver.find_element_by_id("TANGRAM__PSP_10__userName").send_keys(userName)
    # driver.find_element_by_id("TANGRAM__PSP_10__password").send_keys(password)
    # driver.find_element_by_id("TANGRAM__PSP_10__memberPass").click()
    # driver.find_element_by_id("TANGRAM__PSP_10__submit").click()
    # sleep(15)

    ## 登录成功
    print("登录成功")

    return driver

