from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm



def get_scenic_name_href(city, url, id):

    # 修改页面加载策略
    desiredCapabilities = DesiredCapabilities.CHROME
    desiredCapabilities['pageLoadStrategy'] = 'none'

    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    print(city,' 加载中...')

    driver.get(url)
    time.sleep(5)


    for page in range(1,21):

        for i in tqdm(range(15)):

            # 拖动
            driver.execute_script("document.documentElement.scrollTop=2900")

            scenic_list_element_former = "//ul[@class='scenic-list clearfix']/li["
            scenic_list_element = scenic_list_element_former + str(i+1) + ']/a'

            scenic_list = driver.find_element_by_xpath(scenic_list_element)

            # 景点名字和链接
            scenic_list_href = scenic_list.get_attribute('href')
            scenic_list_name = scenic_list.text

            scenic_name_href_list.append([city, id, scenic_list_name, scenic_list_href])

        # 每页先保存，
        save_csv(scenic_name_href_list)

        print('page',page,'save ok')

        if page != 20:

            # 再翻页
            driver.execute_script("document.documentElement.scrollTop=3100")

            driver.find_element_by_link_text("后一页").click()

            time.sleep(5)

    driver.close()

    time.sleep(6)


def save_csv(scenic_list):

    res = pd.DataFrame(data=scenic_list)

    res.to_csv('scenic_name_href.csv')


# 获取界面的北京景点名字和id
# url = 'http://www.mafengwo.cn/jd/10065/gonglve.html'

# 南京景点和id
# url = 'http://www.mafengwo.cn/jd/10684/gonglve.html'

# 上海
# url = 'http://www.mafengwo.cn/jd/10099/gonglve.html'


if __name__ == '__main__':

    city_url_dict = {'北京':10065,'南京':10684,
                     '上海':10099,'四川':12703}

    scenic_name_href_list = []

    for k, v in city_url_dict.items():

        url_ = 'http://www.mafengwo.cn/jd/' + str(v) + '/gonglve.html'

        get_scenic_name_href(k,url_,v)

        print(k,'ok')