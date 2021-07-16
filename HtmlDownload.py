# -*- coding:utf-8 -*-

import requests
from selenium import webdriver
# import time


class HtmlDownload(object):
    # 获取网页上的所有内容数据
    def download(self, url):
        if url is None:
            return None
        elif url[-10:] == '/1.html***' or url[-10:] == '_1.html***':
            return self.down_selenium(url[:-3])
        else:
            return self.download_requests(url)
        return None

    def down_selenium(self, url):
        # 设置无头浏览器
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options = options)
        # 设置最长请求等待时间
        driver.implicitly_wait(20)
        driver.get(url)
        # 找到所有品牌
        try:
            driver.find_element_by_xpath('//div[@class="brand-muti-more"]//a[@class="J_ViewMore view-more"]').click()
            text_data = self.download_requests(url)
            driver.quit()
            print('××××××××××××××××点击更多××××××××××××××××')
            return text_data
        except:
            text_data = self.download_requests(url)
            driver.quit()
            return text_data

    def download_requests(self, url):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        # print('download_requests  get')
        # 设置请求等待时间
        r = requests.get(url, headers=headers, timeout = 20)
        if r.status_code == 200:
            text_data = r.text
            r.encoding = 'utf-8'
            r.close()
            return text_data
        return None
