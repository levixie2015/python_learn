from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def parData(url, companyName):
    # 打开浏览器
    chrome_options = Options()
    chrome_options.add_argument('headless')
    # 驱动路径
    path = 'E:/PythonPoject/Python3.6/chromedriver.exe'
    # 创建浏览器对象
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    driver.get(url)
    # driver.get_screenshot_as_file("test.png")

    driver.find_element_by_id('query').send_keys(companyName)
    driver.find_element_by_id('search').click()
    # driver.switch_to.frame("enterprise_qixinbao")

    frameId = WebDriverWait(driver, 20, 1, NoSuchElementException).until(
        lambda driver: driver.find_element_by_id("enterprise_qixinbao"))
    driver.switch_to.frame(frameId)

    dataList = []
    data = {}
    leftDts = driver.find_element_by_class_name("business-info-left").find_elements_by_tag_name("dt")
    leftDds = driver.find_element_by_class_name("business-info-left").find_elements_by_tag_name("dd")
    for dt, dd in zip(leftDts, leftDds):
        data[dt.text] = dd.text

    rightDts = driver.find_element_by_class_name("business-info-right").find_elements_by_tag_name("dt")
    rightDds = driver.find_element_by_class_name("business-info-right").find_elements_by_tag_name("dd")
    for dt, dd in zip(rightDts, rightDds):
        data[dt.text] = dd.text

    bottomDts = driver.find_element_by_class_name("business-info-bottom").find_elements_by_tag_name("dt")
    bottomDds = driver.find_element_by_class_name("business-info-bottom").find_elements_by_tag_name("dd")
    for dt, dd in zip(bottomDts, bottomDds):
        data[dt.text] = dd.text
    # driver.quit()
    driver.close()
    return data


if __name__ == '__main__':
    url = "https://baike.baidu.com/"
    companyName = "山东汇峰装备科技股份有限公司"
    data = parData(url, companyName)
    print(data)
