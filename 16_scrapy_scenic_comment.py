
from selenium import webdriver
import time
import pandas as pd
from tqdm import tqdm
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchAttributeException

# 判断标签是否存在
def isElementPresent(driver,element):
    try:
        driver.find_element_by_xpath(element)

    # 发生异常，说明不存在
    except NoSuchAttributeException as e:
        return False
    else:
        return True

def get_comment(poi, poi_url):

    # # 页面加载策略
    # desiredCapabilities = DesiredCapabilities.CHROME
    # desiredCapabilities['pageLoadStrategy'] = 'none'

    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    driver.maximize_window()

    print('加载中...')

    driver.get(poi_url)

    time.sleep(10)


    # 拖动位置
    location_element = "//p[@class='sub']"

    scenic_location_y_num = driver.find_element_by_xpath(location_element).location['y'] - 150

    scenic_location_y = "document.documentElement.scrollTop=" + str(scenic_location_y_num)

    driver.execute_script(scenic_location_y)

    # 获取位置
    scenic_location = driver.find_element_by_xpath(location_element).text

    # 获取评论和时间部分
    for page in range(1,6):

        time.sleep(5)

        # 从1开始，15个
        for i in tqdm(range(15)):

            # 拖动位置
            content_element = "//div[@class='rev-list']/ul/li[" + str(i+1) + ']/p'

            content_location_y_num = driver.find_element_by_xpath(content_element).location['y'] - 150

            content_location_y = "document.documentElement.scrollTop=" + str(content_location_y_num)

            driver.execute_script(content_location_y)

            # 获取评论
            content = driver.find_element_by_xpath(content_element)

            c = content.text.replace('\n', '')

            # 获取时间，先判断图片是否存在,设定时间标签
            img_element = "//div[@class='rev-list']/ul/li[" + str(i+1) + ']/div[2]'

            if driver.find_element_by_xpath(img_element).text == '':
                # 说明图片存在
                time_element = "//div[@class='rev-list']/ul/li[" + str(i + 1) + "]/div[3]/span"
            else:
                time_element = "//div[@class='rev-list']/ul/li[" + str(i + 1) + "]/div[2]/span"


            content_time = driver.find_element_by_xpath(time_element).text

            comment.append([poi,scenic_location,content_time,c])

            print('',i+1, 'li ok')

            time.sleep(1.5)

        print(poi, ' page',page, ' ok!')

        if page != 5:

            # driver.find_element_by_link_text("后一页").click()

            next_page_element = "//a[@class='pi pg-next']"

            next_page = driver.find_element_by_xpath(next_page_element)

            time.sleep(1)

            next_page.click()

            time.sleep(3)
    # 保存
    save_csv(comment)

    driver.close()


def save_csv(comment):

    res = pd.DataFrame(data=comment)

    res.to_csv('comment_06.csv')


if __name__ == '__main__':


    # poi_dict = {'颐和园': 3557, '天坛公园': 3503, '圆明园': 6427, '景山公园': 3562,
    #             '北海公园': 3812, '什刹海': 3472, '香山公园': 3936, '北京奥林匹克公园': 77946,
    #             '地坛公园': 3526, '玉渊潭公园': 4430, '北京植物园': 3731, '北京野生动物园': 890032,
    #             '北京大观园': 6731, '世界公园': 4154, '八大处公园': 3751, '雾灵山森林公园': 4258,
    #             '朝阳公园': 4239, '中山公园': 3912, '北京喇叭沟原始森林公园': 6916, '北京凤凰岭自然风景公园': 4129,
    #             '钓鱼台银杏大道': 6931387, '野鸭湖国家湿地公园': 4385, '北京园博园': 6627932, '紫竹院公园': 3998,
    #             '北京云蒙山国家森林公园': 3490, '北京西山国家森林公园': 6924, '百望山森林公园': 3532, '陶然亭公园': 4412,
    #             '元大都城垣遗址公园': 827688, '北宫国家森林公园': 3955, '北京石景山游乐园': 6413, '蟒山国家森林公园': 6627856,
    #             '北京鹫峰国家森林公园': 4150, '日坛公园': 6936, '南海子公园': 21644, '世界花卉大观园': 21466,
    #             '龙潭公园': 6933, '通州运河公园': 21637, '月坛公园': 3956, '故宫': 3474,
    #             }
    poi_dict = {
                '钓鱼台银杏大道': 6931387, '野鸭湖国家湿地公园': 4385, '北京园博园': 6627932, '紫竹院公园': 3998,
                '北京云蒙山国家森林公园': 3490, '北京西山国家森林公园': 6924, '百望山森林公园': 3532, '陶然亭公园': 4412,
                '元大都城垣遗址公园': 827688, '北宫国家森林公园': 3955, '北京石景山游乐园': 6413, '蟒山国家森林公园': 6627856,
                '北京鹫峰国家森林公园': 4150, '日坛公园': 6936, '南海子公园': 21644, '世界花卉大观园': 21466,
                '龙潭公园': 6933, '通州运河公园': 21637, '月坛公园': 3956, '故宫': 3474,
                }

    comment = []

    for k, v in poi_dict.items():

        poi_url = 'http://www.mafengwo.cn/poi/' + str(v) + '.html'

        get_comment(k, poi_url)


    print('ok')