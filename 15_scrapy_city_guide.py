from selenium import webdriver
import time
import sys
sys.setrecursionlimit(10000)  # set the maximum depth as 10000
from tqdm import tqdm

# 爬取马蜂窝北京攻略

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
print('加载中...')

# 北京id：10065
url = 'https://www.mafengwo.cn/gonglve/ziyouxing/mdd_10065/'

driver.get(url)
time.sleep(5)

# 获取当前窗口句柄，后续切换使用
guide_url_list_windows_handle = driver.current_window_handle
guide_url_list = []
count = 1

for page in range(1, 52):

    if page < 50:
        # 翻页
        next_page = driver.find_element_by_link_text("下一页").click()

        # 拖动至底部
        driver.execute_script("document.documentElement.scrollTop=10000")

        time.sleep(4)

        count = page * 20 + 1

        continue

    # 拖动至顶部
    driver.execute_script("document.documentElement.scrollTop=0")
    print('d')

    # guide_url_list界面
    for i in tqdm(range(20)):

        # 跳回list窗口句柄
        if i != 0:
            driver.close()
            time.sleep(2)
            driver.switch_to.window(guide_url_list_windows_handle)

        guide_url_former = "//div[@class='guide-list']/div["

        guide_url_element = guide_url_former + str(i + 1) + ']/a'

        guide_url = driver.find_element_by_xpath(guide_url_element)

        # 滚动
        driver.execute_script('var q=document.documentElement.scrollTop=' + str((i + 1) * 100))

        # 点击事件
        guide_url.click()

        time.sleep(4)

        # 点击后，窗口跳转
        handle_list = driver.window_handles  # list形式
        driver.switch_to.window(handle_list[1])

        # 拖动
        driver.execute_script("document.documentElement.scrollTop=800")

        # 获取点击后的窗口数据
        l_title_element = "//div[@class='l-topic']/h1"
        l_content_element = "//div[@class='_j_content']"

        l_title = driver.find_element_by_xpath(l_title_element)
        l_content = driver.find_element_by_xpath(l_content_element)

        title_content = l_title.text + '\n' + l_content.text

        save_name = './mafengwo_guide/guide_' + str(count) + '.txt'

        with open(save_name, 'w', encoding='utf-8') as f:
            f.write(title_content)

        print('Page:', page, 'Click:', i + 1, 'Count:', count, '->Ok')

        count += 1

    # 窗口关闭，句柄跳转至list url
    driver.close()
    driver.switch_to.window(guide_url_list_windows_handle)

    # 翻页
    next_page = driver.find_element_by_link_text("下一页").click()
    time.sleep(3)

    # 拖动
    driver.execute_script("document.documentElement.scrollTop=0")

if __name__ == '__main__':

    print()





